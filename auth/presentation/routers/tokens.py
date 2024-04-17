from fastapi import Depends, HTTPException, status, APIRouter, Cookie, Response, Query, Header, Body
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from typing import Annotated

from auth.presentation.dependencies import UOWDepend, get_auth


router = APIRouter()


@router.post("/personal/token", description="Получение access-token при авторизации для аутентификации пользователя")
async def login_for_access_token(uow: UOWDepend,
                                 auth: Depends = Depends(get_auth),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authenticate_user(uow, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = await auth.create_pair_token({'uuid': str(user.uuid)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "refresh_token": refresh_token})


@router.post("/personal/refresh", description="Обновление пары ключей access-token и refresh-token."
                                              "Использовать при ошибке аутентификации пользователя для получения "
                                              "новой пары ключей")
async def refresh_token_regenerate(refresh_token: Annotated[str, Body(alias="Authorization")],
                                   auth: Depends = Depends(get_auth)):
    uuid = await auth.decode_token(refresh_token)
    access_token, refresh_token = await auth.create_pair_token({'uuid': str(uuid)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "refresh_token": refresh_token})
