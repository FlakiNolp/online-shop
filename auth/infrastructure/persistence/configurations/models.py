import decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import FLOAT
from typing import List
import uuid as uuid_pkg
import datetime


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, comment="ID сущности")


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"schema": "public"}
    uuid: Mapped[uuid_pkg.UUID] = mapped_column()
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, comment="Почта пользователя")
    hashed_password: Mapped[str] = mapped_column(nullable=False, comment="Хешированный пароль пользователя")
    role: Mapped[str] = mapped_column(nullable=False, comment="Роль пользователя")
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all")


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {"schema": "public"}
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="Название категории")
    products: Mapped[List["Product"]] = relationship(back_populates="category", lazy="selectin",
                                                     cascade="all")


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = {"schema": "public"}
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название товара")
    description: Mapped[str] = mapped_column(String(350), comment="Описание товара")
    price: Mapped[decimal.Decimal("0.00")] = mapped_column(FLOAT(2), nullable=False, comment="Цена товара")
    quantity: Mapped[int] = mapped_column(nullable=False, comment="Количество товара")
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False,
                                             comment="Внешний ключ id категории")
    category: Mapped["Category"] = relationship(back_populates="products", lazy="selectin",
                                                cascade="all")
    images: Mapped[List["Image"]] = relationship(back_populates="product", lazy="selectin", cascade="all")
    order_products: Mapped[List["OrderProduct"]] = relationship(back_populates="product", lazy="selectin",
                                                                cascade="all")


class Image(Base):
    __tablename__ = 'image'
    __table_args__ = {"schema": "public"}
    name: Mapped[str] = mapped_column(String(75), nullable=False, comment="Название картинки")
    product_id: Mapped[str] = mapped_column(ForeignKey(Product.id), nullable=False, comment="Внешний ключ")
    product: Mapped["Product"] = relationship(back_populates="images", lazy="selectin", cascade="all")


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = {"schema": "public"}
    datetime_of_order: Mapped[datetime.datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False, comment="Внешний ключ id пользователя")
    user: Mapped[User] = relationship(back_populates="orders", lazy="selectin", cascade="all")
    order_products: Mapped[List["OrderProduct"]] = relationship(back_populates="order", lazy="selectin",
                                                                cascade="all")


class OrderProduct(Base):
    __tablename__ = 'order_product'
    __table_args__ = {"schema": "public"}
    order_id: Mapped[int] = mapped_column(ForeignKey(Order.id), nullable=False, comment="Внешний ключ id заказа")
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id), nullable=False, comment="Внешний ключ id товара")
    order: Mapped[Order] = relationship(back_populates="order_products", lazy="selectin", cascade="all")
    product: Mapped[Product] = relationship(back_populates="order_products", lazy="selectin",
                                            cascade="all")
