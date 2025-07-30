"""Models for OxaPay API."""

from .balance import AccountBalanceRequest, AccountBalanceResponse
from .base import OrderDirection, PaginatedResponse, ResultResponse, SortField
from .exchange import (
    ExchangeCalculateRequest,
    ExchangeCalculateResponse,
    ExchangeHistoryRequest,
    ExchangeHistoryResponse,
    ExchangePairsResponse,
    ExchangeRateRequest,
    ExchangeRateResponse,
    ExchangeRequestRequest,
    ExchangeRequestResponse,
    ExchangeType,
)
from .merchant import (
    AcceptedCoinsRequest,
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
    PaymentStatus,
    PaymentType,
    RevokeStaticWalletRequest,
    RevokeStaticWalletResponse,
    StaticWalletListRequest,
    StaticWalletListResponse,
)
from .payout import (
    CreatePayoutRequest,
    CreatePayoutResponse,
    PayoutHistoryRequest,
    PayoutHistoryResponse,
    PayoutInfoRequest,
    PayoutInfoResponse,
    PayoutStatus,
    PayoutType,
)
from .system import (
    PriceResponse,
    SupportedCurrenciesResponse,
    SupportedFiatCurrenciesResponse,
    SupportedNetworksResponse,
)

__all__ = [  # noqa: RUF022
    # Base models
    "ResultResponse",
    "PaginatedResponse",
    "OrderDirection",
    "SortField",
    # Merchant models
    "CreateInvoiceRequest",
    "CreateInvoiceResponse",
    "CreateWhiteLabelRequest",
    "CreateWhiteLabelResponse",
    "CreateStaticWalletRequest",
    "CreateStaticWalletResponse",
    "RevokeStaticWalletRequest",
    "RevokeStaticWalletResponse",
    "StaticWalletListRequest",
    "StaticWalletListResponse",
    "PaymentInfoRequest",
    "PaymentInfoResponse",
    "PaymentHistoryRequest",
    "PaymentHistoryResponse",
    "AcceptedCoinsRequest",
    "AcceptedCoinsResponse",
    "PaymentStatus",
    "PaymentType",
    # Payout models
    "CreatePayoutRequest",
    "CreatePayoutResponse",
    "PayoutInfoRequest",
    "PayoutInfoResponse",
    "PayoutHistoryRequest",
    "PayoutHistoryResponse",
    "PayoutStatus",
    "PayoutType",
    # Balance models
    "AccountBalanceRequest",
    "AccountBalanceResponse",
    # Exchange models
    "ExchangeRateRequest",
    "ExchangeRateResponse",
    "ExchangeCalculateRequest",
    "ExchangeCalculateResponse",
    "ExchangePairsResponse",
    "ExchangeRequestRequest",
    "ExchangeRequestResponse",
    "ExchangeHistoryRequest",
    "ExchangeHistoryResponse",
    "ExchangeType",
    # System models
    "SupportedCurrenciesResponse",
    "SupportedFiatCurrenciesResponse",
    "SupportedNetworksResponse",
    "PriceResponse",
]
