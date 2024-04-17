from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClientSession

from cart.core.application.services.order_product_service import OrderProductService
from cart.core.application.services.user_service import UserService
from cart.presentation.schemas.cart import ProductId
from cart.presentation.dependencies.dependencies import auth_depend, get_mongo, UOWDepend
from cart.core.application.services.cart_service import CartService
from cart.core.application.services.product_service import ProductService
from cart.core.application.services.order_service import OrderService
from cart.presentation.specifications.product_specification import ProductIdSpecification
from cart.presentation.specifications.order_specification import ProductIdSpecification
from cart.presentation.specifications.order_specification import OrderUserIdSpecification
from cart.presentation.specifications.user_specification import UserUUIDSpecification


router = APIRouter()


@router.post("/create-new-order")
async def add_product(user_uuid: auth_depend, uow: UOWDepend, mongo_session=Depends(get_mongo)):
    products_mongo = await CartService.get_all_products(mongo_session, user_uuid)
    products = []
    for i in products_mongo:
        info_product = await ProductService.get_product(uow, ProductIdSpecification.is_satisfied(i.get("product_id")))
        if info_product['quantity'] == 0:
             raise HTTPException(status_code=400, detail=f"{info_product['name']} закончился")
        products.append({"id": int(info_product['id']), 'quantity': i.get("quantity")})
    order = await OrderService.create_new_order(uow, user_uuid=user_uuid, products=products)
    await CartService.clear_all_products(mongo_session, collection=user_uuid)
    return order


@router.get("/get-all-orders")
async def get_all_orders(user_uuid: auth_depend, uow: UOWDepend):
    orders = await OrderProductService.get_all_orders(uow, OrderUserIdSpecification.is_satisfied(
                                                          filters=(await UserService.get_user_by_uuid(uow, UserUUIDSpecification.is_satisfied(user_uuid))).get('id')))
    return orders[0]