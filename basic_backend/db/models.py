import uuid

from enum import Enum
from sqlalchemy import Column,String,Enum as SQLEnum,Integer,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from role import Role

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id=Column(UUID, primary_key=True, default=uuid.uuid4)
    username=Column(String(50),unique=True,nullable=False)
    email=Column(String(50),unique=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    role=Column(SQLEnum(Role))
    balance=Column(Integer,default=0,nullable=False)

class Product(Base):
    __tablename__ = "products"  

    id=Column(UUID, primary_key=True, default=uuid.uuid4)
    name=Column(String,index=True)
    description=Column(String)
    price=Column(Integer)
    quantity=Column(Integer)

class Order(Base):
    __tablename__ = "orders"  

    id=Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID,ForeignKey('users.id'))
    product_id=Column(UUID,ForeignKey('products.id'))
    quantity=Column(Integer)

    user = relationship("User")
    product=relationship("Product")