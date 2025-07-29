from typing import Optional

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.aggregate_roots import AuthUser
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.otp import OtpType
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.otp import ABCOtpGenerator
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.abc_api import ABCApi
from ed_auth.application.contracts.infrastructure.abc_email_templater import \
    ABCEmailTemplater
from ed_auth.application.features.auth.dtos.unverified_user_dto import \
    UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators.login_user_dto_validator import \
    LoginUserDtoValidator
from ed_auth.application.features.auth.requests.commands.login_user_command import \
    LoginUserCommand
from ed_auth.application.services.otp_service import CreateOtpDto, OtpService

LOG = get_logger()


@request_handler(LoginUserCommand, BaseResponse[UnverifiedUserDto])
class LoginUserCommandHandler(RequestHandler):
    def __init__(
        self,
        api: ABCApi,
        uow: ABCAsyncUnitOfWork,
        otp: ABCOtpGenerator,
        password: ABCPasswordHandler,
        email_templater: ABCEmailTemplater,
    ):
        self._api = api
        self._uow = uow
        self._otp = otp
        self._password = password
        self._email_templater = email_templater

        self._dto_validator = LoginUserDtoValidator()
        self._otp_service = OtpService(uow)

        self._error_message = "Login failed."
        self._success_message = "Login successful. A one time password been sent."

    async def handle(
        self, request: LoginUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        dto_validator = self._dto_validator.validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                self._error_message,
                dto_validator.errors,
            )

        email, phone_number = request.dto.get("email", ""), request.dto.get(
            "phone_number", ""
        )

        async with self._uow.transaction():
            user = await self._verify_user_is_not_none(email, phone_number)
            await self._verify_password(
                user.password_hash, request.dto.get("password", None)
            )

            if previously_sent_otp := await self._uow.otp_repository.get(
                user_id=user.id
            ):
                await self._uow.otp_repository.delete(previously_sent_otp.id)

            created_otp = await self._otp_service.create(
                CreateOtpDto(
                    user_id=user.id,
                    value=self._otp.generate(),
                    otp_type=OtpType.LOGIN,
                )
            )

        LOG.info(
            f"Created OTP for user {user.id} with value {created_otp.value}")
        notification_response = await self._api.notification_api.send_notification(
            {
                "user_id": user.id,
                "message": self._email_templater.login(
                    user.first_name, created_otp.value
                ),
                "notification_type": NotificationType.EMAIL,
            }
        )

        LOG.info(f"Notification response for user {user.id}")
        if not notification_response["is_success"]:
            LOG.error(
                f"Failed to send OTP to user {user.id}: {notification_response['errors']}"
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                self._error_message,
                ["System failed to send OTP."],
            )

        return BaseResponse[UnverifiedUserDto].success(
            self._success_message,
            UnverifiedUserDto(**user.__dict__),
        )

    async def _verify_user_is_not_none(self, email: str, phone_number: str) -> AuthUser:
        user = (
            await self._uow.auth_user_repository.get(email=email)
            if email
            else await self._uow.auth_user_repository.get(phone_number=phone_number)
        )

        if user is None:
            raise ApplicationException(
                Exceptions.NotFoundException,
                self._error_message,
                ["No user found with the given credentials."],
            )

        return user

    async def _verify_password(
        self, password_hash: str, password: Optional[str]
    ) -> None:
        if password_hash:
            if password is None:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    self._error_message,
                    ["Password is required."],
                )

            if not self._password.verify(password, password_hash):
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    self._error_message,
                    ["Password is incorrect."],
                )
