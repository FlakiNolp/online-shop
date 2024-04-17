from typing import Annotated
from fastapi import Depends
from functools import lru_cache
from datetime import timedelta

from api.infrastructure.persistence.utils.unit_of_work import UnitOfWork
from api.core.application.abstract_classes.abstract_unit_of_work import AbstractUnitOfWork
from api.infrastructure.utils.email_notify import EmailNotify
from api.infrastructure.utils.registration import Registration
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS

UOWDepend = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


@lru_cache()
def get_registration() -> Registration:
    return Registration(SECRET_KEY, ALGORITHM, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


@lru_cache()
def get_email_notify() -> EmailNotify:
    return EmailNotify('smtp.gmail.com', 'check.telegram.bot@gmail.com', 'zetv ahti ckyi bjyn',
                       587)
