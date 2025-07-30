"""FastAPI integration for OxaPay webhook handling."""

import hashlib
import hmac
import json
import logging
from collections.abc import Callable
from collections.abc import Callable as CallableType
from datetime import datetime
from typing import Annotated, Any, TypeVar

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


class WebhookEvent(BaseModel):
    """Base model for webhook events."""

    status: str
    track_id: Annotated[str, Field(validation_alias="trackId")]
    type: str


class PaymentWebhookEvent(WebhookEvent):
    """Model for payment webhook events."""

    amount: float
    currency: str
    fee_paid_by_payer: Annotated[bool, Field(validation_alias="feePaidByPayer")]
    under_paid_cover: Annotated[bool, Field(validation_alias="underPaidCover")]
    email: Annotated[str | None, Field(None, validation_alias="email")]
    order_id: Annotated[str | None, Field(None, validation_alias="orderId")]
    description: Annotated[str | None, Field(None)]
    date: datetime
    pay_date: Annotated[datetime | None, Field(None, validation_alias="payDate")]
    address: Annotated[str | None, Field(None)]
    sender_address: Annotated[str | None, Field(None, validation_alias="senderAddress")]
    tx_id: Annotated[str | None, Field(None, validation_alias="txID")]
    price: Annotated[str | None, Field(None)]
    pay_amount: Annotated[str | None, Field(None, validation_alias="payAmount")]
    pay_currency: Annotated[str | None, Field(None, validation_alias="payCurrency")]
    network: Annotated[str | None, Field(None)]

    class Config:  # noqa: D106
        json_encoders = {datetime: lambda dt: dt.isoformat()}  # noqa: RUF012


class PayoutWebhookEvent(WebhookEvent):
    """Model for payout webhook events."""

    tx_id: Annotated[str | None, Field(None, validation_alias="txID")]
    address: str
    amount: float
    currency: str
    price: Annotated[float | None, Field(None)]
    network: str
    date: datetime
    description: Annotated[str | None, Field(None)]

    class Config:  # noqa: D106
        json_encoders = {datetime: lambda dt: dt.isoformat()}  # noqa: RUF012


WebhookEventType = PaymentWebhookEvent | PayoutWebhookEvent


class WebhookRouter:
    """A class for handling OxaPay webhooks with custom callbacks.

    This class allows setting up callbacks for different webhook events.
    """

    def __init__(
        self,
        app: FastAPI,
        merchant_api_key: str | None = None,
        payout_api_key: str | None = None,
        path: str = "/oxapay/webhook",
    ) -> None:
        """Initialize the webhook router.

        Args:
            app: The FastAPI application
            merchant_api_key: API key for merchant operations (payment webhooks)
            payout_api_key: API key for payout operations (payout webhooks)
            path: The path where the webhook will be set up

        """
        self.app = app
        self.merchant_api_key = merchant_api_key
        self.payout_api_key = payout_api_key
        self.path = path

        # Callbacks for different webhook events
        self.payment_waiting_callback = None
        self.payment_confirming_callback = None
        self.payment_paid_callback = None
        self.payment_expired_callback = None
        self.payment_failed_callback = None

        self.payout_confirming_callback = None
        self.payout_complete_callback = None
        self.payout_rejected_callback = None

        # Set up the webhook handler
        self._setup_webhook_handler()

    def on_payment_waiting(
        self,
        callback: Callable[[PaymentWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payment waiting events.

        Args:
            callback: Function to call when a payment waiting event is received

        Returns:
            The callback function

        """
        self.payment_waiting_callback = callback
        return callback

    def on_payment_confirming(
        self,
        callback: Callable[[PaymentWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payment confirming events.

        Args:
            callback: Function to call when a payment confirming event is received

        Returns:
            The callback function

        """
        self.payment_confirming_callback = callback
        return callback

    def on_payment_paid(
        self,
        callback: Callable[[PaymentWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payment paid events.

        Args:
            callback: Function to call when a payment paid event is received

        Returns:
            The callback function

        """
        self.payment_paid_callback = callback
        return callback

    def on_payment_expired(
        self,
        callback: Callable[[PaymentWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payment expired events.

        Args:
            callback: Function to call when a payment expired event is received

        Returns:
            The callback function

        """
        self.payment_expired_callback = callback
        return callback

    def on_payment_failed(
        self,
        callback: Callable[[PaymentWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payment failed events.

        Args:
            callback: Function to call when a payment failed event is received

        Returns:
            The callback function

        """
        self.payment_failed_callback = callback
        return callback

    def on_payout_confirming(
        self,
        callback: Callable[[PayoutWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payout confirming events.

        Args:
            callback: Function to call when a payout confirming event is received

        Returns:
            The callback function

        """
        self.payout_confirming_callback = callback
        return callback

    def on_payout_complete(
        self,
        callback: Callable[[PayoutWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payout complete events.

        Args:
            callback: Function to call when a payout complete event is received

        Returns:
            The callback function

        """
        self.payout_complete_callback = callback
        return callback

    def on_payout_rejected(
        self,
        callback: Callable[[PayoutWebhookEvent], Any],
    ) -> Callable:
        """Register a callback for payout rejected events.

        Args:
            callback: Function to call when a payout rejected event is received

        Returns:
            The callback function

        """
        self.payout_rejected_callback = callback
        return callback

    def _setup_webhook_handler(self) -> None:
        @self.app.post(self.path)
        async def webhook_handler(request: Request) -> dict[str, str]:
            return await self._process_webhook_request(request)

    def _verify_signature(self, api_key: str, request: Request) -> bool:
        if not api_key:
            return False

        hmac_header = request.headers.get("HMAC")
        if not hmac_header:
            return False

        payload = request.scope["body"].decode("utf-8")
        calculated_hmac = hmac.new(
            api_key.encode(),
            payload.encode(),
            hashlib.sha512,
        ).hexdigest()

        return calculated_hmac == hmac_header

    def _raise_api_key_error(self, event_type: str) -> None:
        detail = (
            "Merchant API key not configured"
            if event_type == "payment"
            else "Payout API key not configured"
        )
        raise HTTPException(status_code=500, detail=detail)

    def _raise_unknown_event_type(self, event_type: str) -> None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown event type: {event_type}",
        )

    def _raise_invalid_signature(self) -> None:
        raise HTTPException(status_code=401, detail="Invalid signature")

    def _parse_webhook_data(
        self,
        data: dict[str, Any],
        event_model: type[WebhookEventType],
    ) -> WebhookEventType:
        try:
            return event_model.parse_obj(data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid webhook payload: {e!s}",
            ) from e

    def _handle_payment_event(self, event: PaymentWebhookEvent) -> None:
        handlers = {
            "Waiting": self.payment_waiting_callback,
            "Confirming": self.payment_confirming_callback,
            "Paid": self.payment_paid_callback,
            "Expired": self.payment_expired_callback,
            "Failed": self.payment_failed_callback,
        }

        if callback := handlers.get(event.status):
            self.call_callback_wrapper(callback, event)

    def _handle_payout_event(self, event: PayoutWebhookEvent) -> None:
        handlers = {
            "Confirming": self.payout_confirming_callback,
            "Complete": self.payout_complete_callback,
            "Rejected": self.payout_rejected_callback,
        }

        if callback := handlers.get(event.status):
            self.call_callback_wrapper(callback, event)

    async def _process_webhook_request(
        self,
        request: Request,
    ) -> dict[str, str]:
        # Read and parse the raw request body
        body = await request.body()
        request.scope["body"] = body  # Store the raw body for signature verification

        try:
            data = json.loads(body)
            event_type = data.get("type")

            # Determine API key and event model based on event type
            if event_type == "payment":
                if not self.merchant_api_key:
                    self._raise_api_key_error(event_type)
                api_key = self.merchant_api_key
                event_model = PaymentWebhookEvent
                handler = self._handle_payment_event
            elif event_type == "payout":
                if not self.payout_api_key:
                    self._raise_api_key_error(event_type)
                api_key = self.payout_api_key
                event_model = PayoutWebhookEvent
                handler = self._handle_payout_event
            else:
                self._raise_unknown_event_type(event_type)

            # Verify the webhook signature
            if not self._verify_signature(api_key, request):
                self._raise_invalid_signature()

            # Parse and validate the webhook data
            event = self._parse_webhook_data(data, event_model)

            # Handle the event
            handler(event)

            # Return a success response
            return {"status": "ok"}  # noqa: TRY300
        except json.JSONDecodeError as err:
            # Print error
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON payload",
            ) from err
        except HTTPException:
            # Re-raise HTTPExceptions without modification
            raise
        except Exception as e:
            logger.exception("Error processing webhook")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing webhook: {e!s}",
            ) from e

    async def _call_callback(
        self,
        callback: CallableType,
        event: WebhookEventType,
    ) -> None:
        try:
            import inspect

            if inspect.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)
        except Exception:
            # Log the error but don't fail the webhook response
            logger.exception("Error in webhook callback")

    def call_callback_wrapper(
        self,
        callback: CallableType,
        event: WebhookEventType,
    ) -> None:
        """Handle calling callbacks in both sync and async contexts.

        Args:
            callback: The callback function to call
            event: The webhook event to pass to the callback

        """
        import asyncio

        try:
            asyncio.create_task(self._call_callback(callback, event))  # noqa: RUF006
        except RuntimeError:
            # We're not in an async context, create a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._call_callback(callback, event))
            loop.close()
