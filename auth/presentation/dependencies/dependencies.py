from typing import Annotated
from fastapi import Depends
from datetime import timedelta
from functools import lru_cache

from auth.infrastructure.persistence.utils.unit_of_work import UnitOfWork
from auth.core.application.abstract_classes.abstract_unit_of_work import AbstractUnitOfWork
from auth.infrastructure.utils.auth import Auth
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS

UOWDepend = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


@lru_cache()
def get_auth() -> Auth:
    return Auth(SECRET_KEY, ALGORITHM, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS))
