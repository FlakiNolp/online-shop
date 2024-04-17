from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClientSession
import json

from cart.presentation.schemas.cart import ProductId
from cart.presentation.dependencies.dependencies import auth_depend, get_mongo, UOWDepend
from cart.core.application.services.cart_service import CartService
from cart.core.application.services.product_service import ProductService
from cart.presentation.specifications.product_specification import ProductIdSpecification


router = APIRouter()


@router.put("/add-to-cart")
async def add_product(product: ProductId, user_uuid: auth_depend, uow: UOWDepend, mongo_session=Depends(get_mongo)):
    info_product = await ProductService.get_product(uow, ProductIdSpecification.is_satisfied(product.product_id))
    if info_product["quantity"] == 0:
        raise HTTPException(status_code=400, detail="Товар закончился")
    await CartService.add_to_cart(mongo_session, product, user_uuid, info_product['quantity'])


@router.delete("/delete-from-cart")
async def delete_product(product: ProductId, user_uuid: auth_depend, uow: UOWDepend, mongo_session=Depends(get_mongo)):
    await CartService.remove_one_product(mongo_session, product, user_uuid)


@router.get("/get-from-cart")
async def get_from_cart(uow: UOWDepend, user_uuid: auth_depend, mongo_session=Depends(get_mongo)):
    products_cart = await CartService.get_all_products(mongo_session=mongo_session, collection=user_uuid)
    products = await ProductService.get_many_products_with_params(uow, ProductIdSpecification.is_satisfied([i['product_id'] for i in products_cart]))
    for key, value in products.items():
        for i in products_cart:
            if key == i['product_id']:
                products[key]['quantity'] = i['quantity']
    return products
