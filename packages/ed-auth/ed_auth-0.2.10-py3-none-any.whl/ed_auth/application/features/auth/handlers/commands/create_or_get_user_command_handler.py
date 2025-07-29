from datetime import UTC, datetime

from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.aggregate_roots import AuthUser
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos import CreateOrGetUserDto
from ed_auth.application.features.auth.dtos.validators import \
    CreateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateOrGetUserCommand
from ed_auth.common.generic_helpers import get_new_id

LOG = get_logger()


@request_handler(CreateOrGetUserCommand, BaseResponse[CreateOrGetUserDto])
class CreateOrGetUserCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
    ):
        self._uow = uow
        self._dto_validator = CreateUserDtoValidator()

        self._success_message = "User returned successfully."
        self._error_message = "User couldn't be found or created."

    async def handle(
        self, request: CreateOrGetUserCommand
    ) -> BaseResponse[CreateOrGetUserDto]:
        dto_validation_response = self._dto_validator.validate(request.dto)

        if not dto_validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                self._error_message,
                dto_validation_response.errors,
            )

        phone_number = request.dto.get("phone_number")

        if phone_number is None:
            raise ApplicationException(
                Exceptions.ValidationException,
                self._error_message,
                ["Phone number is required"],
            )

        dto = request.dto

        async with self._uow.transaction():
            existing_user = await self._uow.auth_user_repository.get(
                phone_number=phone_number
            )

            if existing_user:
                return BaseResponse[CreateOrGetUserDto].success(
                    self._success_message,
                    CreateOrGetUserDto(**existing_user.__dict__, new=False),
                )

            user = await self._uow.auth_user_repository.create(
                AuthUser(
                    id=get_new_id(),
                    first_name=dto["first_name"],
                    last_name=dto["last_name"],
                    email=dto.get("email", ""),
                    phone_number=dto.get("phone_number", ""),
                    password_hash="",
                    verified=True,
                    create_datetime=datetime.now(UTC),
                    update_datetime=datetime.now(UTC),
                    deleted=False,
                    logged_in=False,
                    deleted_datetime=None,
                )
            )

        return BaseResponse[CreateOrGetUserDto].success(
            self._success_message,
            CreateOrGetUserDto(**user.__dict__, new=True),
        )
