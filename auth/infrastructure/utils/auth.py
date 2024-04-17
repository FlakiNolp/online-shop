from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib

from auth.core.application.abstract_classes.abstract_unit_of_work import AbstractUnitOfWork
from auth.core.application.services.user_service import UserService
from auth.presentation.specifications.user_specification import UserFormSpecification
from auth.core.domain.entity.user import User
from auth.infrastructure.persistence.configurations.models import User


class Auth:
    def __init__(self, secret_key: str, algorithm: str, access_token_expire: timedelta,
                 refresh_token_expire: timedelta):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.access_token_expire = access_token_expire
        self.refresh_token_expire = refresh_token_expire

    def __set__(self, instance, value):
        instance.__dict__["__secret_key"] = value

    def __get__(self, instance, name: str):
        return instance.__dict__[name]

    async def authenticate_user(self, uow: AbstractUnitOfWork, email: str, password: str) -> User | bool:
        user = await UserService().get(uow, UserFormSpecification.is_satisfied(email=email))
        if not user or not hashlib.sha256(password.encode()).hexdigest() == user.hashed_password:
            return False
        return user

    async def create_pair_token(self, data: dict):
        access_token = await self.create_token(data, expires_delta=self.access_token_expire)
        refresh_token = await self.create_token(data, expires_delta=self.refresh_token_expire)
        return access_token, refresh_token

    async def create_token(self, data: dict, expires_delta: timedelta = None):
        if expires_delta:
            data.update({"exp": datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(data, self.__secret_key, algorithm=self.__algorithm)
        return encoded_jwt

    async def decode_token(self, token: str):
        try:
            uuid = (jwt.decode(token, self.__secret_key, algorithms=self.__algorithm)).get("uuid")
            if uuid is None:
                raise JWTError
            return uuid
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
