from fastapi import Depends, APIRouter, Response, BackgroundTasks, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from api.core.application.services.user_service import UserService
from api.presentation.specifications.user_specification import UserFormSpecification
from api.presentation.dependencies import UOWDepend, get_email_notify, get_registration
from api.core.domain.schemas.user import User

router = APIRouter()


@router.post("/sign-up", description="Регистрация пользователя")
async def sign_up(uow: UOWDepend, background_tasks: BackgroundTasks, email=Depends(get_email_notify),
                  registration=Depends(get_registration),
                  form_data: OAuth2PasswordRequestForm = Depends()):
    if tasks := await UserService().send_registration_email(uow, email_notify=email, form_data=form_data,
                                                            background_tasks=background_tasks,
                                                            specification=UserFormSpecification.is_satisfied(
                                                                form_data.username), registration=registration):
        return Response(status_code=200, background=tasks)


@router.get("/registration")
async def registration(uow: UOWDepend, registration=Depends(get_registration),
                       token: str = Query()):
    email, hashed_password = await registration.decode_registration_token(token)
    await UserService().add(uow, User(email=email, hashed_password=hashed_password, role="User"))
    return RedirectResponse(url="http://192.168.3.11/login")
