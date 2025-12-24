from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    brand: str
    stock: int
    rating: Optional[float] = 0.0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    stock: Optional[int] = None
    rating: Optional[float] = None

class Product(ProductBase):
    id: int
    image_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class ProfileUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None