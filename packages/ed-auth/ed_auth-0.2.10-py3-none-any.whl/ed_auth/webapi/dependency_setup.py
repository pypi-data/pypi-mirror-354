from typing import Annotated

from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.jwt import ABCJwtHandler
from ed_domain.utils.otp import ABCOtpGenerator
from ed_domain.utils.security.password import ABCPasswordHandler
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork
from ed_infrastructure.utils.jwt import JwtHandler
from ed_infrastructure.utils.otp import OtpGenerator
from ed_infrastructure.utils.password import PasswordHandler
from ed_notification.documentation.api.notification_api_client import \
    NotificationApiClient
from fastapi import Depends
from rmediator.mediator import Mediator

from ed_auth.application.contracts.infrastructure.abc_api import ABCApi
from ed_auth.application.contracts.infrastructure.abc_email_templater import \
    ABCEmailTemplater
from ed_auth.application.contracts.infrastructure.abc_rabbitmq_producer import \
    ABCRabbitMQProducers
from ed_auth.application.features.auth.handlers.commands import (
    CreateOrGetUserCommandHandler, CreateUserCommandHandler,
    CreateUserVerifyCommandHandler, DeleteUserCommandHandler,
    LoginUserCommandHandler, LoginUserVerifyCommandHandler,
    VerifyTokenCommandHandler)
from ed_auth.application.features.auth.handlers.commands.logout_user_command_handler import \
    LogoutUserCommandHandler
from ed_auth.application.features.auth.handlers.commands.update_user_command_handler import \
    UpdateUserCommandHandler
from ed_auth.application.features.auth.requests.commands import (
    CreateOrGetUserCommand, CreateUserCommand, CreateUserVerifyCommand,
    DeleteUserCommand, LoginUserCommand, LoginUserVerifyCommand,
    VerifyTokenCommand)
from ed_auth.application.features.auth.requests.commands.logout_user_command import \
    LogoutUserCommand
from ed_auth.application.features.auth.requests.commands.update_user_command import \
    UpdateUserCommand
from ed_auth.common.generic_helpers import get_config
from ed_auth.common.typing.config import Config, Environment
from ed_auth.infrastructure.api_handler import ApiHandler
from ed_auth.infrastructure.email_templater import EmailTemplater
from ed_auth.infrastructure.rabbitmq_producers import RabbitMQProducers


async def get_rabbitmq_producers(
    config: Annotated[Config, Depends(get_config)],
) -> ABCRabbitMQProducers:
    producers = RabbitMQProducers(config)
    await producers.start()

    return producers


def email_templater() -> ABCEmailTemplater:
    return EmailTemplater()


def get_api_client(config: Annotated[Config, Depends(get_config)]) -> ABCApi:
    return ApiHandler(NotificationApiClient(config["notification_api"]))


def get_uow(config: Annotated[Config, Depends(get_config)]) -> ABCAsyncUnitOfWork:
    return UnitOfWork(config["db"])


def get_jwt(config: Annotated[Config, Depends(get_config)]) -> ABCJwtHandler:
    return JwtHandler(config["jwt"]["secret"], config["jwt"]["algorithm"])


def get_otp(config: Annotated[Config, Depends(get_config)]) -> ABCOtpGenerator:
    return OtpGenerator(dev_mode=config["env"] != Environment.PROD)


def get_password(config: Annotated[Config, Depends(get_config)]) -> ABCPasswordHandler:
    return PasswordHandler(config["password_scheme"])


def mediator(
    email_templater: Annotated[ABCEmailTemplater, Depends(email_templater)],
    api: Annotated[ABCApi, Depends(get_api_client)],
    uow: Annotated[ABCAsyncUnitOfWork, Depends(get_uow)],
    jwt: Annotated[ABCJwtHandler, Depends(get_jwt)],
    otp: Annotated[ABCOtpGenerator, Depends(get_otp)],
    password: Annotated[ABCPasswordHandler, Depends(get_password)],
) -> Mediator:
    mediator = Mediator()

    auth_handlers = [
        (
            CreateUserCommand,
            CreateUserCommandHandler(uow, otp, password),
        ),
        (
            CreateOrGetUserCommand,
            CreateOrGetUserCommandHandler(uow),
        ),
        (CreateUserVerifyCommand, CreateUserVerifyCommandHandler(uow, jwt)),
        (
            LoginUserCommand,
            LoginUserCommandHandler(api, uow, otp, password, email_templater),
        ),
        (LoginUserVerifyCommand, LoginUserVerifyCommandHandler(uow, jwt)),
        (LogoutUserCommand, LogoutUserCommandHandler(uow, jwt)),
        (VerifyTokenCommand, VerifyTokenCommandHandler(uow, jwt)),
        (DeleteUserCommand, DeleteUserCommandHandler(uow)),
        (UpdateUserCommand, UpdateUserCommandHandler(uow, password)),
    ]
    for request, handler in auth_handlers:
        mediator.register_handler(request, handler)

    return mediator
