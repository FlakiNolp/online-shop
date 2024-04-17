from fastapi import HTTPException, status
from jose import JWTError, jwt


class Auth:
    def __init__(self, secret_key: str, algorithm: str):
        self.__secret_key = secret_key
        self.__algorithm = algorithm

    def __set__(self, instance, value):
        instance.__dict__["__secret_key"] = value

    def __get__(self, instance, name: str):
        return instance.__dict__[name]

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
