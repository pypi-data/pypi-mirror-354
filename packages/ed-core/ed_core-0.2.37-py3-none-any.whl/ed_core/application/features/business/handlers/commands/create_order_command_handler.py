from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_domain.common.logging import get_logger
from ed_domain.core.aggregate_roots import Consumer
from ed_domain.core.entities.notification import NotificationType
from ed_domain.persistence.async_repositories.abc_async_unit_of_work import \
    ABCAsyncUnitOfWork
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_core.application.common.responses.base_response import BaseResponse
from ed_core.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_core.application.features.business.dtos.validators import \
    CreateOrderDtoValidator
from ed_core.application.features.business.requests.commands import \
    CreateOrderCommand
from ed_core.application.features.common.dtos import OrderDto
from ed_core.application.services.consumer_service import ConsumerService
from ed_core.application.services.order_service import OrderService

LOG = get_logger()

BILL_AMOUNT = 10


@request_handler(CreateOrderCommand, BaseResponse[OrderDto])
class CreateOrderCommandHandler(RequestHandler):
    def __init__(
        self,
        uow: ABCAsyncUnitOfWork,
        api: ABCApi,
    ):
        self._uow = uow
        self._api = api

        self._order_service = OrderService(uow)
        self._consumer_service = ConsumerService(uow)

        self._error_message = "Failed to create order"

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]:
        dto, business_id, consumer_id = (
            request.dto,
            request.business_id,
            request.dto.consumer_id,
        )
        dto_validator = CreateOrderDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                self._error_message,
                dto_validator.errors,
            )

        async with self._uow.transaction():
            consumer = await self._consumer_service.get(consumer_id)
            assert consumer is not None

            order = await self._order_service.create_order(
                dto, business_id, BILL_AMOUNT
            )
            order_dto = await self._order_service.to_dto(order)

        await self._send_notification(consumer)

        return BaseResponse[OrderDto].success(
            "Order created successfully.",
            order_dto,
        )

    async def _send_notification(self, consumer: Consumer) -> None:
        LOG.info(f"Sending notification to consumer {consumer.user_id}")
        notification_response = await self._api.notification_api.send_notification(
            {
                "user_id": consumer.user_id,
                "notification_type": NotificationType.EMAIL,
                "message": f"Dear {consumer.first_name}, an order has been created for you. More information will be provided soon.",
            }
        )
        LOG.info(
            f"Got response from notification api sent successfully {notification_response}."
        )
