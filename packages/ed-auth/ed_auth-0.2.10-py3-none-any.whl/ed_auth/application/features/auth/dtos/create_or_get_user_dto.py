from typing import NotRequired, TypedDict
from uuid import UUID


class CreateOrGetUserDto(TypedDict):
    id: UUID
    first_name: str
    last_name: str
    email: NotRequired[str]
    phone_number: NotRequired[str]
    new: bool
