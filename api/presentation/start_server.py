from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from api.presentation.routers import user, catalog
from api.infrastructure.persistence.utils.db import SQLAlchemyDataBase
from api.infrastructure.persistence.configurations.models import User, Product, Order, OrderProduct, Category, Image


app = FastAPI()
database = SQLAlchemyDataBase()
admin = Admin(app, engine=database._async_engine)
app.include_router(user.router)
app.include_router(catalog.router)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.uuid, User.role, User.email, User.hashed_password]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.description, Product.price, Product.category_id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.datetime_of_order, Order.user_id]


class OrderProductAdmin(ModelView, model=OrderProduct):
    column_list = [OrderProduct.id, OrderProduct.product_id, OrderProduct.order_id]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]


class ImageAdmin(ModelView, model=Image):
    column_list = [Image.id, Image.name, Image.product_id]


admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderProductAdmin)
admin.add_view(ImageAdmin)
admin.add_view(CategoryAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.3.11", "http://192.168.3.11:1000", "http://192.168.3.11:1002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.3.11", port=1000)
