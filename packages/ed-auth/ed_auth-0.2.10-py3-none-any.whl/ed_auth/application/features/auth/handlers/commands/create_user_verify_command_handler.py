from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.entities.otp import OtpType
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.tokens.auth_payload import AuthPayload, UserType
from ed_domain.utils.jwt import ABCJwtHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import UserDto
from ed_auth.application.features.auth.dtos.validators.create_user_verify_dto_validator import \
    CreateUserVerifyDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateUserVerifyCommand

LOG = get_logger()


@request_handler(CreateUserVerifyCommand, BaseResponse[UserDto])
class CreateUserVerifyCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        jwt: ABCJwtHandler[AuthPayload],
    ):
        self._uow = uow
        self._jwt = jwt
        self._dto_validator = CreateUserVerifyDtoValidator()

    async def handle(self, request: CreateUserVerifyCommand) -> BaseResponse[UserDto]:
        dto_validation_response = self._dto_validator.validate(request.dto)

        if not dto_validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Otp verification failed.",
                dto_validation_response.errors,
            )

        dto = request.dto

        async with self._uow.transaction():
            user = await self._uow.auth_user_repository.get(id=dto["user_id"])

            if not user:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "Otp verification failed.",
                    [f"User with that id = {dto['user_id']} does not exist."],
                )

            otp = await self._uow.otp_repository.get(user_id=dto["user_id"])

        if not otp or otp.otp_type != OtpType.VERIFY_EMAIL:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Otp verification failed.",
                [
                    f"Otp has not been sent to the user with id = {dto['user_id']} recently."
                ],
            )

        if otp.value != dto["otp"]:
            raise ApplicationException(
                Exceptions.BadRequestException,
                "Otp verification failed.",
                ["Otp does not match with the one sent."],
            )

        token = self._jwt.encode(
            AuthPayload(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email or "",
                phone_number=user.phone_number or "",
                user_type=UserType.DRIVER,
            )
        )
        return BaseResponse[UserDto].success(
            "Create successful.",
            UserDto(**user.__dict__, token=token),
        )
