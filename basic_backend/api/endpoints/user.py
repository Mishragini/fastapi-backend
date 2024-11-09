from fastapi import APIRouter
from db.database import get_db
from db.models import User, Product, Order
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from auth import get_current_user
from pydantic import BaseModel
from uuid import UUID  

class BuyProduct(BaseModel):
   quantity:int

class Onramp(BaseModel):
   inr:float

user_router = APIRouter()

@user_router.post("/onramp")
def onramp_money(onrampBody:Onramp,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
   db_user=db.query(User).filter(User.id == current_user.id).first()
   if not db_user:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND, 
           detail="User not found"
       )
   
   if onrampBody.inr <= 0:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Amount must be greater than 0"
       )
   
   amount_in_paise = int(onrampBody.inr * 100)
   db_user.balance += amount_in_paise
   
   db.commit()
   
   return {
       "message": "Balance updated successfully",
       "new_balance": db_user.balance / 100  
   }
   

@user_router.post("/buy/{product_id}")
def buy_product(product_id:UUID,buyBody:BuyProduct,current_user:User=Depends(get_current_user),db:Session= Depends(get_db)):
  product=db.query(Product).filter(Product.id == product_id).first()
  if not product:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") 
  
  total_cost=product.price*buyBody.quantity

  if total_cost>current_user.balance:
     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
     

  if product.quantity< buyBody.quantity:
     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient product quantity")
  
  new_order = Order(
     user_id=current_user.id,
     product_id=product_id,
     quantity=buyBody.quantity
  )

  db.add(new_order)
  product.quantity -= buyBody.quantity
  current_user.balance -= total_cost
  db.commit()
    
  return {"message": "Product purchased successfully!"}


@user_router.get("/myOrders")
def get_orders(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
   orders = db.query(Order).filter(Order.user_id == current_user.id).all()
   return [
        {
            "id": str(order.id),
            "product_id": str(order.product_id),
            "quantity": order.quantity,
            "user_id": str(order.user_id)
        } for order in orders
    ]




