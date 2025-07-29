from typing import Type

from ed_domain.common.logging import get_logger
from ed_infrastructure.documentation.message_queue.rabbitmq.rabbitmq_multiple_queue_producers import \
    RabbitMQMultipleQueuesProducer

from ed_auth.application.features.auth.dtos import (CreateUserDto,
                                                    DeleteUserDto,
                                                    UpdateUserDto)
from ed_auth.documentation.message_queue.rabbitmq.abc_auth_rabbitmq_subscriber import (
    ABCAuthRabbitMQSubscriber, AuthQueues)
from ed_auth.documentation.message_queue.rabbitmq.auth_queue_descriptions import \
    AuthQueueDescriptions

LOG = get_logger()


class AuthRabbitMQSubscriber(ABCAuthRabbitMQSubscriber):
    def __init__(self, connection_url: str) -> None:
        self._connection_url = connection_url
        descriptions = AuthQueueDescriptions(connection_url).descriptions

        all_auth_queue_names = []
        producer_generic_model: Type[object] = object
        for desc in descriptions:
            if "request_model" in desc:
                all_auth_queue_names.append(
                    desc["connection_parameters"]["queue"])

        if all_auth_queue_names:
            producer_url = descriptions[0]["connection_parameters"]["url"]
            self._auth_producer = RabbitMQMultipleQueuesProducer[
                producer_generic_model
            ](
                url=producer_url,
                queues=all_auth_queue_names,
            )
        else:
            LOG.warning(
                "No auth queue descriptions found. Auth producer not initialized."
            )
            self._auth_producer = None

    async def create_user(self, create_user_dto: CreateUserDto) -> None:
        if not self._auth_producer:
            LOG.error("Auth producer not initialized. Cannot create user.")
            return

        LOG.info(
            f"Publishing create_user_dto to {AuthQueues.CREATE_USER} queue.")
        await self._auth_producer.publish(create_user_dto, AuthQueues.CREATE_USER.value)

    async def delete_user(self, delete_user_dto: DeleteUserDto) -> None:
        if not self._auth_producer:
            LOG.error("Auth producer not initialized. Cannot delete user.")
            return

        LOG.info(
            f"Publishing delete_user_dto to {AuthQueues.DELETE_USER} queue.")
        await self._auth_producer.publish(delete_user_dto, AuthQueues.DELETE_USER.value)

    async def update_user(self, update_user_dto: UpdateUserDto) -> None:
        if not self._auth_producer:
            LOG.error("Auth producer not initialized. Cannot update user.")
            return

        LOG.info(
            f"Publishing update_user_dto to {AuthQueues.UPDATE_USER} queue.")
        await self._auth_producer.publish(update_user_dto, AuthQueues.UPDATE_USER.value)

    async def start(self) -> None:
        LOG.info("Starting Auth RabbitMQ producer.")
        if self._auth_producer:
            try:
                await self._auth_producer.start()
                LOG.info(
                    f"Auth producer started and declared queues: {self._auth_producer._queues}"
                )
            except Exception as e:
                LOG.error(f"Failed to start Auth producer: {e}")
                raise
        else:
            LOG.info("No Auth producer to start.")

    def stop_producers(self) -> None:
        LOG.info("Stopping Auth RabbitMQ producer.")
        if self._auth_producer:
            self._auth_producer.stop()
        else:
            LOG.info("No Auth producer to stop.")
