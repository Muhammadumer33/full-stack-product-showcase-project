from database import SessionLocal
import models
import auth

db = SessionLocal()
try:
    user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if user:
        print("Updating existing admin user...")
        user.hashed_password = auth.get_password_hash("admin123")
    else:
        print("Creating new admin user...")
        hashed_password = auth.get_password_hash("admin123")
        user = models.User(email="admin@example.com", hashed_password=hashed_password)
        db.add(user)
    
    db.commit()
    print("SUCCESS: Admin user set to admin@example.com / admin123")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    db.close()
