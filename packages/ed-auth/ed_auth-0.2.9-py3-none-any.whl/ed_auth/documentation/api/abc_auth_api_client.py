from abc import ABCMeta, abstractmethod
from uuid import UUID

from ed_domain.documentation.api.definitions import ApiResponse

from ed_auth.application.features.auth.dtos import (CreateOrGetUserDto,
                                                    CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    LogoutDto,
                                                    UnverifiedUserDto,
                                                    UpdateUserDto, UserDto,
                                                    VerifyTokenDto)


class ABCAuthApiClient(metaclass=ABCMeta):
    # Auth features
    @abstractmethod
    async def create_or_get_user(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[CreateOrGetUserDto]: ...

    @abstractmethod
    async def create_get_otp(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[UnverifiedUserDto]: ...

    @abstractmethod
    async def create_verify_otp(
        self, create_user_verify_dto: CreateUserVerifyDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    async def login_get_otp(
        self, login_user_dto: LoginUserDto
    ) -> ApiResponse[UnverifiedUserDto]: ...

    @abstractmethod
    async def login_verify_otp(
        self, login_user_verify_dto: LoginUserVerifyDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    async def verify_token(
        self, verify_token_dto: VerifyTokenDto
    ) -> ApiResponse[UserDto]: ...

    @abstractmethod
    async def logout(self, logout_dto: LogoutDto) -> ApiResponse[None]: ...

    # User features
    @abstractmethod
    async def delete_user(self, id: UUID) -> ApiResponse[None]: ...

    @abstractmethod
    async def update_user(
        self, id: UUID, update_user_dto: UpdateUserDto
    ) -> ApiResponse[UserDto]: ...
