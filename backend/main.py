from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, auth
from database import engine, get_db
import shutil
import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Showcase API")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to create admin user
@app.on_event("startup")
def create_admin_user():
    db = next(get_db())
    try:
        user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not user:
            hashed_password = auth.get_password_hash("admin123")
            admin_user = models.User(email="admin@example.com", hashed_password=hashed_password)
            db.add(admin_user)
            db.commit()
            print("Admin user created: admin@example.com / admin123")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Product Showcase API", "version": "1.0"}

# Login endpoint
@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Login attempt: username={form_data.username}, password={form_data.password}")
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    print(f"User found: {user}")
    if user:
        is_correct = auth.verify_password(form_data.password, user.hashed_password)
        print(f"Password correct: {is_correct}")
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Get all products
@app.get("/api/products", response_model=List[schemas.Product])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    
    if category:
        query = query.filter(models.Product.category == category)
    
    if search:
        query = query.filter(models.Product.name.contains(search))
    
    products = query.offset(skip).limit(limit).all()
    return products

# Get single product
@app.get("/api/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Create product with image (PROTECTED)
@app.post("/api/products", response_model=schemas.Product)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    brand: str = Form(...),
    stock: int = Form(...),
    rating: float = Form(0.0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    image_path = None
    
    # Handle image upload
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{name.replace(' ', '_')}_{int(time.time())}{file_extension}"
        file_path = UPLOAD_DIR / file_name
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_path = f"/uploads/{file_name}"
    
    # Create product
    db_product = models.Product(
        name=name,
        description=description,
        price=price,
        category=category,
        brand=brand,
        stock=stock,
        rating=rating,
        image_path=image_path
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Update product (PROTECTED)
@app.put("/api/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[str] = Form(None),
    brand: Optional[str] = Form(None),
    stock: Optional[int] = Form(None),
    rating: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    if name: product.name = name
    if description: product.description = description
    if price: product.price = price
    if category: product.category = category
    if brand: product.brand = brand
    if stock is not None: product.stock = stock
    if rating is not None: product.rating = rating
    
    # Handle new image upload
    if image:
        # Delete old image if exists
        if product.image_path:
            old_file = Path(product.image_path.lstrip('/'))
            if old_file.exists():
                old_file.unlink()
        
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{name or product.name}_{int(time.time())}{file_extension}".replace(' ', '_')
        file_path = UPLOAD_DIR / file_name
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        product.image_path = f"/uploads/{file_name}"
    
    db.commit()
    db.refresh(product)
    return product

# Delete product (PROTECTED)
@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete image file if exists
    if product.image_path:
        file_path = Path(product.image_path.lstrip('/'))
        if file_path.exists():
            file_path.unlink()
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Change Password (PROTECTED)
@app.post("/api/change-password")
def change_password(
    password_data: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify current password
    if not auth.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.hashed_password = auth.get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# Get categories
@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Product.category).distinct().all()
    return [cat[0] for cat in categories]

# ===== USER MANAGEMENT ENDPOINTS =====

# Get all users (PROTECTED)
@app.get("/api/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    users = db.query(models.User).all()
    return users

# Create user (PROTECTED)
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = auth.get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update user (PROTECTED)
@app.put("/api/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user.email = user_data.email
    
    if user_data.name is not None:
        user.name = user_data.name
    
    if user_data.password:
        user.hashed_password = auth.get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(user)
    return user

# Delete user (PROTECTED)
@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Update own profile (PROTECTED)
@app.put("/api/profile", response_model=schemas.UserResponse)
def update_profile(
    profile_data: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if email is being changed and if it's already taken
    if profile_data.email and profile_data.email != current_user.email:
        existing_user = db.query(models.User).filter(models.User.email == profile_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = profile_data.email
    
    if profile_data.name is not None:
        current_user.name = profile_data.name
    
    db.commit()
    db.refresh(current_user)
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
