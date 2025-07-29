from typing import NotRequired, TypedDict
from uuid import UUID


class UpdateUserDto(TypedDict):
    id: UUID
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    phone_number: NotRequired[str]
    password: NotRequired[str]
    email: NotRequired[str]
