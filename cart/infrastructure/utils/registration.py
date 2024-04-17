from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
import hashlib


class Registration:
    def __init__(self, secret_key: str, algorithm: str, registration_token_expire: timedelta):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.registration_token_expire = registration_token_expire

    def __set__(self, instance, value):
        instance.__dict__["__secret_key"] = value

    def __get__(self, instance, name: str):
        return instance.__dict__[name]

    async def create_registration_token(self, data: dict, expires_delta: timedelta = None):
        data.update({"hashed_password": hashlib.sha256(data.get("hashed_password").encode()).hexdigest()})
        if expires_delta:
            data.update({"exp": datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(data, self.__secret_key, algorithm=self.__algorithm)
        return encoded_jwt

    async def decode_registration_token(self, token: str):
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=self.__algorithm)
            email: str = payload.get(f"email")
            hashed_password = payload.get(f"hashed_password")
            if email is None or hashed_password is None:
                raise JWTError
            return email, hashed_password
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
