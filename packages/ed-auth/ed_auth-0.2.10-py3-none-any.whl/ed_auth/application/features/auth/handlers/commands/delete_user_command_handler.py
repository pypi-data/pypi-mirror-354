from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.features.auth.requests.commands import \
    DeleteUserCommand

LOG = get_logger()


@request_handler(DeleteUserCommand, BaseResponse[None])
class DeleteUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCAsyncUnitOfWork):
        self._uow = uow

    async def handle(self, request: DeleteUserCommand) -> BaseResponse[None]:
        async with self._uow.transaction():
            if await self._uow.auth_user_repository.get(id=request.id) is None:
                raise ApplicationException(
                    Exceptions.NotFoundException,
                    "User deletion failed.",
                    ["User not found."],
                )

            deleted = await self._uow.auth_user_repository.delete(request.id)

        if not deleted:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "User deletion failed.",
                ["Internal server error."],
            )

        return BaseResponse[None].success(
            "User deleted successfully.",
            None,
        )
