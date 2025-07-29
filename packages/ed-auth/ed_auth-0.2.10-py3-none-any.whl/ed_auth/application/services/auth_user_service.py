from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

from ed_domain.common.logging import get_logger
from ed_domain.core.aggregate_roots import AuthUser
from ed_domain.persistence.async_repositories import ABCAsyncUnitOfWork
from ed_domain.utils.security.password import ABCPasswordHandler

from ed_auth.application.features.auth.dtos.create_user_dto import \
    CreateUserDto
from ed_auth.application.features.auth.dtos.unverified_user_dto import \
    UnverifiedUserDto
from ed_auth.application.features.auth.dtos.update_user_dto import \
    UpdateUserDto
from ed_auth.application.features.auth.dtos.user_dto import UserDto
from ed_auth.application.services.abc_service import ABCService
from ed_auth.common.generic_helpers import get_new_id

LOG = get_logger()


class UserService(
    ABCService[
        AuthUser,
        CreateUserDto,
        UpdateUserDto,
        UserDto,
    ]
):
    def __init__(self, uow: ABCAsyncUnitOfWork, password_handler: ABCPasswordHandler):
        super().__init__("User", uow.auth_user_repository)

        self._password_handler = password_handler

        LOG.info("UserService initialized with UnitOfWork.")

    async def get_by_phone_number(self, phone_number: str) -> Optional[AuthUser]:
        return await self._repository.get(phone_number=phone_number)

    async def get_by_email(self, email: str) -> Optional[AuthUser]:
        return await self._repository.get(email=email)

    async def create(self, dto: CreateUserDto) -> AuthUser:
        hashed_password = (
            self._password_handler.hash(
                dto["password"]) if "password" in dto else ""
        )

        user = AuthUser(
            id=get_new_id(),
            first_name=dto["first_name"],
            last_name=dto["last_name"],
            email=dto.get("email", ""),
            phone_number=dto.get("phone_number", ""),
            password_hash=hashed_password,
            verified=False,
            create_datetime=datetime.now(UTC),
            update_datetime=datetime.now(UTC),
            deleted=False,
            logged_in=False,
            deleted_datetime=None,
        )
        user = await self._repository.create(user)
        LOG.info(f"User created with ID: {user.id}")
        return user

    async def update(self, id: UUID, dto: UpdateUserDto) -> Optional[AuthUser]:
        user = await self._repository.get(id=id)
        if user is None:
            LOG.error(f"Cannot update: No user found for ID: {id}")
            return None

        if "first_name" in dto:
            user.first_name = dto["first_name"]
        if "last_name" in dto:
            user.last_name = dto["last_name"]
        if "phone_number" in dto:
            user["phone_number"] = dto["phone_number"]
        if "email" in dto:
            user.email = dto["email"]
        if "password" in dto:
            user.password = self._password_handler.hash(dto["password"])

        user.update_datetime = datetime.now(UTC)
        await self._repository.save(user)
        LOG.info(f"User with ID: {id} updated.")
        return user

    async def to_dto_with_token(self, entity: AuthUser, token: str) -> UserDto:
        return UserDto(
            {
                "id": entity.id,
                "first_name": entity.first_name,
                "last_name": entity.last_name,
                "phone_number": entity.phone_number or "",
                "email": entity.email or "",
                "token": token,
            }
        )

    async def to_unverified_user_dto(self, entity: AuthUser) -> UnverifiedUserDto:
        return UnverifiedUserDto(
            {
                "id": entity.id,
                "first_name": entity.first_name,
                "last_name": entity.last_name,
                "phone_number": entity.phone_number or "",
                "email": entity.email or "",
            }
        )
