from fastapi import APIRouter
from db.database import get_db
from db.models import User,Product
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from auth import get_current_user
from role import Role
from pydantic import BaseModel

class AddProduct(BaseModel):
    name:str
    description:str
    price:float
    quantity:int

admin_router = APIRouter()

@admin_router.post("/product")
def create_product(product:AddProduct,current_user:User=Depends(get_current_user),db:Session= Depends(get_db)):
    if(current_user.role != Role.admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create products")
    
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price * 100,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {
        "id": str(new_product.id),
        "message": "Product created successfully!"
    }
    


