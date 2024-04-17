from fastapi import Depends, APIRouter, Response, BackgroundTasks, Query
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm

from api.presentation.schemas.product import GetProduct
from api.presentation.dependencies.dependencies import UOWDepend
from api.core.application.services.product_service import ProductService
from api.core.application.services.category_service import CategoryService
from api.presentation.specifications.product_specification import ProductsFilterSpecification, ProductNameSpecification

router = APIRouter()


@router.get("/catalog")
async def catalog(uow: UOWDepend, params: GetProduct = Depends()):
    res = await ProductService.get_many_products_with_params(uow, ProductsFilterSpecification.is_satisfied(params))
    return res


@router.get("/get-categories")
async def get_categories(uow: UOWDepend):
    res = await CategoryService.get_categories(uow)
    return res


@router.get("/product/{product_name}")
async def get_product(product_name: str, uow: UOWDepend):
    res = await ProductService.get_product(uow, ProductNameSpecification.is_satisfied(product_name))
    return res
