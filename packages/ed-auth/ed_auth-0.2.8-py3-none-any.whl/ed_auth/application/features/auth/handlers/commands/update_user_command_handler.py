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
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.update_user_dto import \
    UpdateUserDto
from ed_auth.application.features.auth.dtos.user_dto import UserDto
from ed_auth.application.features.auth.dtos.validators import \
    UpdateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    UpdateUserCommand

LOG = get_logger()


@request_handler(UpdateUserCommand, BaseResponse[UserDto])
class UpdateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork, password: ABCPasswordHandler):
        self._uow = uow
        self._dto_validator = UpdateUserDtoValidator()
        self._password = password

    async def handle(self, request: UpdateUserCommand) -> BaseResponse[UserDto]:
        validation_response = self._dto_validator.validate(request.dto)

        if not validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                validation_response.errors,
            )

        async with self._uow.transaction():
            user = await self._uow.auth_user_repository.get(id=request.id)
            if user is None:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "User update failed.",
                    ["User not found."],
                )

            dto = request.dto
            await self._uow.auth_user_repository.update(
                id=user.id,
                entity=AuthUser(
                    id=user.id,
                    create_datetime=user.create_datetime,
                    update_datetime=datetime.now(UTC),
                    deleted=user.deleted,
                    first_name=dto.get("first_name") or user.first_name,
                    last_name=dto.get("last_name") or user.last_name,
                    email=dto.get("email") or user.email,
                    phone_number=dto.get("phone_number") or user.phone_number,
                    password_hash=self._password.hash(dto.get("password", ""))
                    or user.password_hash,
                    verified=user.verified,
                    logged_in=user.logged_in,
                    deleted_datetime=None,
                ),
            )

            return BaseResponse[UserDto].success(
                "User updated successfully.",
                UserDto(**user.__dict__),
            )
