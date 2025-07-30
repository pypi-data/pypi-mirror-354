# ruff: noqa: F405

"""Synchronous wrappers for OxaPay async API client."""

import asyncio
import types
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from .client import OxaPayClient
from .models import *  # noqa: F403

T = TypeVar("T")


def sync_wrapper(func: Callable[..., T]) -> Callable[..., T]:
    """Convert an async function to a sync function.

    Args:
        func: The async function to convert

    Returns:
        A synchronous wrapper that runs the async function in an event loop

    """

    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If there's no event loop in the current thread, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper


class SyncOxaPayClient:
    """Synchronous wrapper for OxaPayClient.

    Provides the same methods as OxaPayClient but in a synchronous manner.
    """

    def __init__(
        self,
        merchant_api_key: str | None = None,
        payout_api_key: str | None = None,
        general_api_key: str | None = None,
    ) -> None:
        """Initialize the sync OxaPay client.

        Args:
            merchant_api_key: API key for merchant operations
            payout_api_key: API key for payout operations
            general_api_key: API key for general operations like exchange

        """
        self._async_client = OxaPayClient(
            merchant_api_key=merchant_api_key,
            payout_api_key=payout_api_key,
            general_api_key=general_api_key,
        )

    def __enter__(self) -> "SyncOxaPayClient":
        """Enter context manager.

        Returns:
            The SyncOxaPayClient instance

        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Exit context manager.

        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised

        """

    # Merchant API Methods

    @sync_wrapper
    async def create_invoice(
        self,
        request: CreateInvoiceRequest,
    ) -> CreateInvoiceResponse:
        """Create a new payment link.

        Args:
            request: Invoice creation parameters

        Returns:
            Invoice creation response with payment link and tracking ID

        """
        return await self._async_client.create_invoice(request)

    @sync_wrapper
    async def create_white_label_payment(
        self,
        request: CreateWhiteLabelRequest,
    ) -> CreateWhiteLabelResponse:
        """Create a white-labeled payment.

        Args:
            request: White-label payment creation parameters

        Returns:
            White-label payment response with payment details

        """
        return await self._async_client.create_white_label_payment(request)

    @sync_wrapper
    async def create_static_wallet(
        self,
        request: CreateStaticWalletRequest,
    ) -> CreateStaticWalletResponse:
        """Create a static wallet address.

        Args:
            request: Static wallet creation parameters

        Returns:
            Static wallet address creation response

        """
        return await self._async_client.create_static_wallet(request)

    @sync_wrapper
    async def revoke_static_wallet(
        self,
        request: RevokeStaticWalletRequest,
    ) -> RevokeStaticWalletResponse:
        """Revoke a static wallet address.

        Args:
            request: Static wallet revocation parameters

        Returns:
            Static wallet revocation response

        """
        return await self._async_client.revoke_static_wallet(request)

    @sync_wrapper
    async def get_static_wallets(
        self,
        request: StaticWalletListRequest,
    ) -> StaticWalletListResponse:
        """Get a list of static wallets.

        Args:
            request: Static wallet list request parameters

        Returns:
            List of static wallets with pagination info

        """
        return await self._async_client.get_static_wallets(request)

    @sync_wrapper
    async def get_payment_info(self, track_id: str | int) -> PaymentInfoResponse:
        """Get information about a specific payment.

        Args:
            track_id: The payment tracking ID

        Returns:
            Payment information

        """
        return await self._async_client.get_payment_info(track_id)

    @sync_wrapper
    async def get_payment_history(
        self,
        request: PaymentHistoryRequest,
    ) -> PaymentHistoryResponse:
        """Get payment history.

        Args:
            request: Payment history request parameters

        Returns:
            Payment history with pagination info

        """
        return await self._async_client.get_payment_history(request)

    @sync_wrapper
    async def get_accepted_coins(self) -> AcceptedCoinsResponse:
        """Get a list of accepted cryptocurrencies.

        Returns:
            List of accepted cryptocurrency symbols

        """
        return await self._async_client.get_accepted_coins()

    # Payout API Methods

    @sync_wrapper
    async def create_payout(self, request: CreatePayoutRequest) -> CreatePayoutResponse:
        """Create a new payout.

        Args:
            request: Payout creation parameters

        Returns:
            Payout creation response with tracking ID

        """
        return await self._async_client.create_payout(request)

    @sync_wrapper
    async def get_payout_info(self, track_id: str | int) -> PayoutInfoResponse:
        """Get information about a specific payout.

        Args:
            track_id: The payout tracking ID

        Returns:
            Payout information

        """
        return await self._async_client.get_payout_info(track_id)

    @sync_wrapper
    async def get_payout_history(
        self,
        request: PayoutHistoryRequest,
    ) -> PayoutHistoryResponse:
        """Get payout history.

        Args:
            request: Payout history request parameters

        Returns:
            Payout history with pagination info

        """
        return await self._async_client.get_payout_history(request)

    @sync_wrapper
    async def get_account_balance(
        self,
        currency: str | None = None,
    ) -> AccountBalanceResponse:
        """Get account balance for all or a specific currency.

        Args:
            currency: Specific currency to get balance for (optional)

        Returns:
            Account balance information

        """
        return await self._async_client.get_account_balance(currency)

    # Exchange API Methods

    @sync_wrapper
    async def get_exchange_rate(
        self,
        request: ExchangeRateRequest,
    ) -> ExchangeRateResponse:
        """Get exchange rate between two currencies.

        Args:
            request: Exchange rate request parameters

        Returns:
            Exchange rate information

        """
        return await self._async_client.get_exchange_rate(request)

    @sync_wrapper
    async def calculate_exchange(
        self,
        request: ExchangeCalculateRequest,
    ) -> ExchangeCalculateResponse:
        """Calculate exchange amount.

        Args:
            request: Exchange calculation request parameters

        Returns:
            Exchange calculation result

        """
        return await self._async_client.calculate_exchange(request)

    @sync_wrapper
    async def get_exchange_pairs(self) -> ExchangePairsResponse:
        """Get available exchange pairs.

        Returns:
            List of available exchange pairs

        """
        return await self._async_client.get_exchange_pairs()

    @sync_wrapper
    async def create_exchange_request(
        self,
        request: ExchangeRequestRequest,
    ) -> ExchangeRequestResponse:
        """Create a new exchange request.

        Args:
            request: Exchange request parameters

        Returns:
            Exchange request creation response

        """
        return await self._async_client.create_exchange_request(request)

    @sync_wrapper
    async def get_exchange_history(
        self,
        request: ExchangeHistoryRequest,
    ) -> ExchangeHistoryResponse:
        """Get exchange history.

        Args:
            request: Exchange history request parameters

        Returns:
            Exchange history with pagination info

        """
        return await self._async_client.get_exchange_history(request)

    # System API Methods

    @sync_wrapper
    async def get_prices(self) -> PriceResponse:
        """Get current prices of all supported cryptocurrencies.

        Returns:
            Current prices information

        """
        return await self._async_client.get_prices()

    @sync_wrapper
    async def get_supported_currencies(self) -> SupportedCurrenciesResponse:
        """Get a list of supported currencies.

        Returns:
            List of supported currencies with network details

        """
        return await self._async_client.get_supported_currencies()

    @sync_wrapper
    async def get_supported_fiat_currencies(self) -> SupportedFiatCurrenciesResponse:
        """Get a list of supported fiat currencies.

        Returns:
            List of supported fiat currencies

        """
        return await self._async_client.get_supported_fiat_currencies()

    @sync_wrapper
    async def get_supported_networks(self) -> SupportedNetworksResponse:
        """Get a list of supported blockchain networks.

        Returns:
            List of supported networks

        """
        return await self._async_client.get_supported_networks()

    @sync_wrapper
    async def check_system_status(self) -> str:
        """Check if the OxaPay API is operational.

        Returns:
            Status message (usually "OK")

        """
        return await self._async_client.check_system_status()

    def verify_webhook_signature(
        self,
        signature: str,
        payload: str,
        *,
        is_payment: bool = True,
    ) -> bool:
        """Verify the HMAC signature of a webhook payload.

        Args:
            signature: The HMAC signature from the webhook header
            payload: The raw webhook payload
            is_payment: Whether this is a payment webhook (True) or payout webhook (False)

        Returns:
            True if the signature is valid, False otherwise

        """  # noqa: E501
        return self._async_client.verify_webhook_signature(
            signature,
            payload,
            is_payment=is_payment,
        )
