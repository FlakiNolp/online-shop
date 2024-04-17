from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/collection")
async def collection(request: Request):
    return templates.TemplateResponse("collection.html", {"request": request})


@router.get("/sign-up")
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/cart")
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@router.get('/order')
async def order(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})


@router.get("/static/{path}")
async def static(path: str):
    return FileResponse(path=fr'C:\Users\maksi\PycharmProjects\Masha_project\front\static\{path}')


@router.get("/{path}/{path1}")
async def static1(path: str, path1: str):
    return FileResponse(path=fr'C:\Users\maksi\PycharmProjects\Masha_project\front\templates\{path}\{path1}')
