#admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from models import Product, ProductCreate, ProductUpdate, ProductResponse, User, UserResponse
from database import get_session
from auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    users = session.exec(select(User)).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Cannot delete admin users")
    
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}

@router.get("/stats")
async def get_admin_stats(
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    # Get total users
    total_users = session.exec(select(User)).count()
    
    # Get total products
    total_products = session.exec(select(Product)).count()
    
    # Get low stock products
    low_stock_products = session.exec(
        select(Product).where(Product.stock < 10)
    ).all()
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "low_stock_products": len(low_stock_products),
        "low_stock_items": [
            {"id": p.id, "name": p.name, "stock": p.stock} 
            for p in low_stock_products
        ]
    }