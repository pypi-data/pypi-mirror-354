from enum import StrEnum
from typing import TypedDict


class Environment(StrEnum):
    TEST = "test"
    DEV = "development"
    STAGING = "staging"
    PROD = "prod"


class DbConfig(TypedDict):
    user: str
    password: str
    db: str
    host: str


class RabbitMQConfig(TypedDict):
    url: str


class JwtConfig(TypedDict):
    secret: str
    algorithm: str


class Config(TypedDict):
    db: DbConfig
    rabbitmq: RabbitMQConfig
    jwt: JwtConfig
    password_scheme: str
    env: Environment
    notification_api: str


class TestMessage(TypedDict):
    title: str
