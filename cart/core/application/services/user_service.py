from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy
from fastapi import HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

import cart.core.domain.schemas.user
from cart.core.application.abstract_classes import abstract_unit_of_work
from cart.core.application.abstract_classes.abstract_specification import AbstractSpecification
from cart.infrastructure.utils.email_notify import EmailNotify
from cart.infrastructure.utils.registration import Registration


class UserService:
    @staticmethod
    async def get_user_by_uuid(uow: abstract_unit_of_work.AbstractUnitOfWork, specification: AbstractSpecification.is_satisfied) -> dict:
        try:
            async with uow:
                return await uow.user.get_one(specification)
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(e)

    @staticmethod
    async def add(uow: abstract_unit_of_work.AbstractUnitOfWork, user: cart.core.domain.schemas.user.User):
        try:
            async with uow:
                user_uuid = await uow.user.add(data=user.model_dump())
                await uow.commit()
                return user_uuid
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                                detail="User already exist, try log-in")

    @staticmethod
    async def send_registration_email(uow: abstract_unit_of_work.AbstractUnitOfWork,
                                      email_notify: EmailNotify,
                                      form_data: OAuth2PasswordRequestForm,
                                      background_tasks: BackgroundTasks,
                                      specification: AbstractSpecification.is_satisfied,
                                      registration: Registration):
        try:
            async with uow:
                await uow.user.get_one(specification)
                raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                                    detail="User already exist, try log-in")
        except sqlalchemy.exc.NoResultFound:
            text = f"Перейдите по ссылке, чтобы завершить процесс регистрации\n\nhttp://192.168.3.11:8080/registration?token=" \
                          f"{await registration.create_registration_token({"email": form_data.username,
                                                                           "hashed_password": form_data.password})}\n\nСсылка действительна 10 минут"
            background_tasks.add_task(email_notify.send_mail, form_data.username, text)
            return background_tasks
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
