from uuid import UUID

from ed_domain.documentation.api.definitions import ApiResponse
from ed_infrastructure.documentation.api.endpoint_client import EndpointClient

from ed_auth.application.features.auth.dtos import (CreateOrGetUserDto,
                                                    CreateUserDto,
                                                    CreateUserVerifyDto,
                                                    LoginUserDto,
                                                    LoginUserVerifyDto,
                                                    LogoutDto,
                                                    UnverifiedUserDto,
                                                    UpdateUserDto, UserDto,
                                                    VerifyTokenDto)
from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.api.auth_endpoint_descriptions import \
    AuthEndpointDescriptions


class AuthApiClient(ABCAuthApiClient):
    def __init__(self, auth_api: str) -> None:
        self._driver_endpoints = AuthEndpointDescriptions(auth_api)

    async def create_or_get_user(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[CreateOrGetUserDto]:
        endpoint = self._driver_endpoints.get_description("create_or_get_user")
        api_client = EndpointClient[CreateOrGetUserDto](endpoint)

        return await api_client({"request": create_user_dto})

    async def create_get_otp(
        self, create_user_dto: CreateUserDto
    ) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description("create_get_otp")
        api_client = EndpointClient[UnverifiedUserDto](endpoint)

        return await api_client({"request": create_user_dto})

    async def create_verify_otp(
        self, create_user_verify_dto: CreateUserVerifyDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("create_verify_otp")
        api_client = EndpointClient[UserDto](endpoint)

        return await api_client({"request": create_user_verify_dto})

    async def login_get_otp(
        self, login_user_dto: LoginUserDto
    ) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description("login_get_otp")
        api_client = EndpointClient[UnverifiedUserDto](endpoint)

        return await api_client({"request": login_user_dto})

    async def login_verify_otp(
        self, login_user_verify_dto: LoginUserVerifyDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("login_verify_otp")
        api_client = EndpointClient[UserDto](endpoint)

        return await api_client({"request": login_user_verify_dto})

    async def verify_token(
        self, verify_token_dto: VerifyTokenDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("verify_token")
        api_client = EndpointClient[UserDto](endpoint)

        return await api_client({"request": verify_token_dto})

    async def logout(self, logout_dto: LogoutDto) -> ApiResponse[None]:
        endpoint = self._driver_endpoints.get_description("logout")
        api_client = EndpointClient[None](endpoint)

        return await api_client({"request": logout_dto})

    async def delete_user(self, id: UUID) -> ApiResponse[None]:
        endpoint = self._driver_endpoints.get_description("delete_user")
        api_client = EndpointClient[None](endpoint)

        return await api_client({"path_params": {"user_id": str(id)}})

    async def update_user(
        self, id: UUID, update_user_dto: UpdateUserDto
    ) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description("update_user")
        api_client = EndpointClient[UserDto](endpoint)

        return await api_client(
            {"request": update_user_dto, "path_params": {"user_id": str(id)}}
        )


if __name__ == "__main__":
    AuthApiClient("")
