from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from ed_domain.utils.jwt import ABCJwtHandler
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.requests.commands import \
    LogoutUserCommand

LOG = get_logger()


@request_handler(LogoutUserCommand, BaseResponse[None])
class LogoutUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork, jwt: ABCJwtHandler):
        self._uow = uow
        self._jwt = jwt

    async def handle(self, request: LogoutUserCommand) -> BaseResponse[None]:
        payload = self._jwt.decode(request.dto["token"])

        if "email" not in payload:
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Logout failed.",
                ["Token is malformed."],
            )

        async with self._uow.transaction():
            user = await self._uow.auth_user_repository.get(email=payload["email"])
            if user is None:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Logout failed.",
                    ["User is not found."],
                )

            if not user.logged_in:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Logout failed.",
                    ["User is not logged in."],
                )

            user.log_out()
            await self._uow.auth_user_repository.update(user.id, user)

        return BaseResponse[None].success(
            "Logout successful.",
            None,
        )
