#cart.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, List
import json
from datetime import datetime

from models import Cart, CartItem, Order, OrderItem, User, Product
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# In-memory cart storage (in production, use Redis or database)
user_carts: Dict[int, Cart] = {}

@router.get("/", response_model=Cart)
async def get_cart(current_user: User = Depends(get_current_user)):
    cart = user_carts.get(current_user.id, Cart())
    return cart

@router.post("/add", response_model=Cart)
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get product from database
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Get or create user's cart
    cart = user_carts.get(current_user.id, Cart())
    
    # Check if product already in cart
    item_index = None
    for i, item in enumerate(cart.items):
        if item.product_id == product_id:
            item_index = i
            break
    
    if item_index is not None:
        # Update existing item
        cart.items[item_index].quantity += quantity
    else:
        # Add new item
        cart_item = CartItem(
            product_id=product.id,
            quantity=quantity,
            name=product.name,
            price=product.price
        )
        cart.items.append(cart_item)
    
    # Update total
    cart.total = sum(item.price * item.quantity for item in cart.items)
    
    # Save cart
    user_carts[current_user.id] = cart
    
    return cart

@router.post("/checkout")
async def checkout(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    cart = user_carts.get(current_user.id)
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Check stock and process order
    order_items = []
    for item in cart.items:
        product = session.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.name} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )
        
        # Update product stock
        product.stock -= item.quantity
        session.add(product)
        
        # Create order item
        order_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            name=product.name
        )
        order_items.append(order_item)
    
    # Create order
    order = Order(
        user_id=current_user.id,
        items=order_items,
        total=cart.total,
        status="completed"
    )
    
    # Save order to JSON file
    try:
        with open("orders.json", "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []
    
    order_dict = {
        "id": len(orders) + 1,
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "total": order.total,
        "status": order.status,
        "created_at": datetime.utcnow().isoformat()
    }
    
    orders.append(order_dict)
    
    with open("orders.json", "w") as f:
        json.dump(orders, f, indent=2)
    
    # Clear cart
    user_carts[current_user.id] = Cart()
    
    session.commit()
    
    return {
        "message": "Order placed successfully",
        "order_id": order_dict["id"],
        "total": order.total
    }

@router.delete("/item/{product_id}")
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user)
):
    cart = user_carts.get(current_user.id)
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Find and remove item
    cart.items = [item for item in cart.items if item.product_id != product_id]
    
    # Update total
    cart.total = sum(item.price * item.quantity for item in cart.items)
    
    user_carts[current_user.id] = cart
    
    return cart

@router.delete("/clear")
async def clear_cart(current_user: User = Depends(get_current_user)):
    user_carts[current_user.id] = Cart()
    return {"message": "Cart cleared successfully"}