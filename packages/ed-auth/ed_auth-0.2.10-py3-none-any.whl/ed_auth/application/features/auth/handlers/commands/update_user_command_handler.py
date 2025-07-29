from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.security.password import ABCPasswordHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.dtos.user_dto import UserDto
from ed_auth.application.features.auth.dtos.validators import \
    UpdateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    UpdateUserCommand
from ed_auth.application.services.auth_user_service import UserService

LOG = get_logger()


@request_handler(UpdateUserCommand, BaseResponse[UserDto])
class UpdateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork, password: ABCPasswordHandler):
        self._uow = uow
        self._password = password

        self._dto_validator = UpdateUserDtoValidator()
        self._user_service = UserService(uow, password)

        self._error_message = "User account updated failed."
        self._success_message = "User updated successfully."

    async def handle(self, request: UpdateUserCommand) -> BaseResponse[UserDto]:
        validation_response = self._dto_validator.validate(request.dto)

        if not validation_response.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                validation_response.errors,
            )

        async with self._uow.transaction():
            user = await self._user_service.update(request.id, request.dto)
            if user is None:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    self._error_message,
                    [f"User with id: {request.id} not found."],
                )

            user_dto = await self._user_service.to_dto(user)

            return BaseResponse[UserDto].success(self._success_message, user_dto)
