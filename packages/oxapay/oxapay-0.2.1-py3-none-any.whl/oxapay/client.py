"""Main client implementation for OxaPay API."""

import hashlib
import hmac
import types
from typing import Any, TypeVar

import aiohttp
from pydantic import BaseModel

from .exceptions import OxaPayError, OxaPayValidationError
from .models.balance import AccountBalanceRequest, AccountBalanceResponse
from .models.exchange import (
    ExchangeCalculateRequest,
    ExchangeCalculateResponse,
    ExchangeHistoryRequest,
    ExchangeHistoryResponse,
    ExchangePairsResponse,
    ExchangeRateRequest,
    ExchangeRateResponse,
    ExchangeRequestRequest,
    ExchangeRequestResponse,
)
from .models.merchant import (
    AcceptedCoinsResponse,
    CreateInvoiceRequest,
    CreateInvoiceResponse,
    CreateStaticWalletRequest,
    CreateStaticWalletResponse,
    CreateWhiteLabelRequest,
    CreateWhiteLabelResponse,
    PaymentHistoryRequest,
    PaymentHistoryResponse,
    PaymentInfoRequest,
    PaymentInfoResponse,
    RevokeStaticWalletRequest,
    RevokeStaticWalletResponse,
    StaticWalletListRequest,
    StaticWalletListResponse,
)
from .models.payout import (
    CreatePayoutRequest,
    CreatePayoutResponse,
    PayoutHistoryRequest,
    PayoutHistoryResponse,
    PayoutInfoRequest,
    PayoutInfoResponse,
)
from .models.system import (
    PriceResponse,
    SupportedCurrenciesResponse,
    SupportedFiatCurrenciesResponse,
    SupportedNetworksResponse,
)

T = TypeVar("T", bound=BaseModel)


class OxaPayClient:
    """Client for interacting with the OxaPay API.

    Provides methods for all OxaPay API endpoints with proper typing and error handling.
    """

    BASE_URL = "https://api.oxapay.com"
    SUCCESS_RESULT_CODE = 100  # Success result code from API

    def __init__(
        self,
        merchant_api_key: str | None = None,
        payout_api_key: str | None = None,
        general_api_key: str | None = None,
    ) -> None:
        """Initialize the OxaPay client.

        Args:
            merchant_api_key: API key for merchant operations
            payout_api_key: API key for payout operations
            general_api_key: API key for general operations like exchange

        """
        self.merchant_api_key = merchant_api_key
        self.payout_api_key = payout_api_key
        self.general_api_key = general_api_key
        self.session = None

    async def __aenter__(self) -> "OxaPayClient":
        """Enter async context manager.

        Returns:
            The OxaPayClient instance.

        """
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Exit async context manager.

        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised

        """
        if self.session:
            await self.session.close()
            self.session = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """Make a request to the OxaPay API.

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint path
            data: Request data
            response_model: Pydantic model for response validation

        Returns:
            Validated response data or raw response

        Raises:
            OxaPayError: For API errors
            OxaPayValidationError: For validation errors

        """
        url = f"{self.BASE_URL}{endpoint}"

        if self.session is None:
            self.session = aiohttp.ClientSession()
            close_after = True
        else:
            close_after = False

        try:
            async with self.session.request(method, url, json=data) as response:
                response_data = await response.json()

                # Check for API errors
                if (
                    "result" in response_data
                    and response_data["result"] != self.SUCCESS_RESULT_CODE
                ):
                    raise OxaPayError(
                        code=response_data.get("result", 0),
                        message=response_data.get("message", "Unknown error"),
                    )

                # Validate and return the response
                if response_model:
                    try:
                        return response_model.parse_obj(response_data)
                    except Exception as e:
                        msg = f"Response validation error: {e!s}"
                        raise OxaPayValidationError(msg) from e
                return response_data
        finally:
            if close_after:
                await self.session.close()
                self.session = None

    # Merchant API Methods

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/request",
            data=request_data,
            response_model=CreateInvoiceResponse,
        )

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/request/whitelabel",
            data=request_data,
            response_model=CreateWhiteLabelResponse,
        )

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/request/staticaddress",
            data=request_data,
            response_model=CreateStaticWalletResponse,
        )

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/revoke/staticaddress",
            data=request_data,
            response_model=RevokeStaticWalletResponse,
        )

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/list/staticaddress",
            data=request_data,
            response_model=StaticWalletListResponse,
        )

    async def get_payment_info(self, track_id: str | int) -> PaymentInfoResponse:
        """Get information about a specific payment.

        Args:
            track_id: The payment tracking ID

        Returns:
            Payment information

        """
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request = PaymentInfoRequest(trackId=str(track_id))
        request_data = request.model_dump(by_alias=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/inquiry",
            data=request_data,
            response_model=PaymentInfoResponse,
        )

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
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["merchant"] = self.merchant_api_key

        return await self._request(
            "POST",
            "/merchants/list",
            data=request_data,
            response_model=PaymentHistoryResponse,
        )

    async def get_accepted_coins(self) -> AcceptedCoinsResponse:
        """Get a list of accepted cryptocurrencies.

        Returns:
            List of accepted cryptocurrency symbols

        """
        if not self.merchant_api_key:
            msg = "Merchant API key is required"
            raise ValueError(msg)

        request_data = {"merchant": self.merchant_api_key}

        return await self._request(
            "POST",
            "/merchants/allowedCoins",
            data=request_data,
            response_model=AcceptedCoinsResponse,
        )

    # Payout API Methods

    async def create_payout(self, request: CreatePayoutRequest) -> CreatePayoutResponse:
        """Create a new payout.

        Args:
            request: Payout creation parameters

        Returns:
            Payout creation response with tracking ID

        """
        if not self.payout_api_key:
            msg = "Payout API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["key"] = self.payout_api_key

        return await self._request(
            "POST",
            "/api/send",
            data=request_data,
            response_model=CreatePayoutResponse,
        )

    async def get_payout_info(self, track_id: str | int) -> PayoutInfoResponse:
        """Get information about a specific payout.

        Args:
            track_id: The payout tracking ID

        Returns:
            Payout information

        """
        if not self.payout_api_key:
            msg = "Payout API key is required"
            raise ValueError(msg)

        request = PayoutInfoRequest(trackId=str(track_id))
        request_data = request.model_dump(by_alias=True)
        request_data["key"] = self.payout_api_key

        return await self._request(
            "POST",
            "/api/inquiry",
            data=request_data,
            response_model=PayoutInfoResponse,
        )

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
        if not self.payout_api_key:
            msg = "Payout API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["key"] = self.payout_api_key

        return await self._request(
            "POST",
            "/api/list",
            data=request_data,
            response_model=PayoutHistoryResponse,
        )

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
        if not self.payout_api_key:
            msg = "Payout API key is required"
            raise ValueError(msg)

        request = AccountBalanceRequest(currency=currency)
        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["key"] = self.payout_api_key

        return await self._request(
            "POST",
            "/api/balance",
            data=request_data,
            response_model=AccountBalanceResponse,
        )

    # Exchange API Methods

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
        request_data = request.model_dump(by_alias=True)

        return await self._request(
            "POST",
            "/exchange/rate",
            data=request_data,
            response_model=ExchangeRateResponse,
        )

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
        request_data = request.model_dump(by_alias=True)

        return await self._request(
            "POST",
            "/exchange/calculate",
            data=request_data,
            response_model=ExchangeCalculateResponse,
        )

    async def get_exchange_pairs(self) -> ExchangePairsResponse:
        """Get available exchange pairs.

        Returns:
            List of available exchange pairs

        """
        return await self._request(
            "POST",
            "/exchange/pairs",
            response_model=ExchangePairsResponse,
        )

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
        if not self.general_api_key:
            msg = "General API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["key"] = self.general_api_key

        return await self._request(
            "POST",
            "/exchange/request",
            data=request_data,
            response_model=ExchangeRequestResponse,
        )

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
        if not self.general_api_key:
            msg = "General API key is required"
            raise ValueError(msg)

        request_data = request.model_dump(by_alias=True, exclude_none=True)
        request_data["key"] = self.general_api_key

        return await self._request(
            "POST",
            "/exchange/list",
            data=request_data,
            response_model=ExchangeHistoryResponse,
        )

    # System API Methods

    async def get_prices(self) -> PriceResponse:
        """Get current prices of all supported cryptocurrencies.

        Returns:
            Current prices information

        """
        return await self._request("POST", "/api/prices", response_model=PriceResponse)

    async def get_supported_currencies(self) -> SupportedCurrenciesResponse:
        """Get a list of supported currencies.

        Returns:
            List of supported currencies with network details

        """
        return await self._request(
            "POST",
            "/api/currencies",
            response_model=SupportedCurrenciesResponse,
        )

    async def get_supported_fiat_currencies(self) -> SupportedFiatCurrenciesResponse:
        """Get a list of supported fiat currencies.

        Returns:
            List of supported fiat currencies

        """
        return await self._request(
            "POST",
            "/api/fiats",
            response_model=SupportedFiatCurrenciesResponse,
        )

    async def get_supported_networks(self) -> SupportedNetworksResponse:
        """Get a list of supported blockchain networks.

        Returns:
            List of supported networks

        """
        return await self._request(
            "POST",
            "/api/networks",
            response_model=SupportedNetworksResponse,
        )

    async def check_system_status(self) -> str:
        """Check if the OxaPay API is operational.

        Returns:
            Status message (usually "OK")

        """
        response = await self._request("POST", "/monitor")
        return (
            "OK"
            if isinstance(response, dict) and response.get("status") == "ok"
            else str(response)
        )

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
        api_key = self.merchant_api_key if is_payment else self.payout_api_key
        if not api_key:
            key_type = "Merchant" if is_payment else "Payout"
            msg = f"{key_type} API key is required"
            raise ValueError(msg)

        calculated_hmac = hmac.new(
            api_key.encode(),
            payload.encode(),
            hashlib.sha512,
        ).hexdigest()

        return calculated_hmac == signature
