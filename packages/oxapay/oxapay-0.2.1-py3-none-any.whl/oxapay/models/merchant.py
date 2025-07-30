"""Models for OxaPay Merchant API."""

from enum import Enum

from pydantic import BaseModel, Field

from .base import OrderDirection, PaginatedResponse, ResultResponse, SortField


# Common enums
class PaymentType(str, Enum):
    """Payment type enum."""

    INVOICE = "Invoice"
    WHITE_LABEL = "White-Label"
    STATIC_WALLET = "Static Wallet"


class PaymentStatus(str, Enum):
    """Payment status enum."""

    NEW = "New"
    WAITING = "Waiting"
    CONFIRMING = "Confirming"
    PAID = "Paid"
    EXPIRED = "Expired"
    FAILED = "Failed"


# Invoice creation
class CreateInvoiceRequest(BaseModel):
    """Request model for creating an invoice."""

    amount: int | float = Field(..., description="The amount for the payment")
    currency: str | None = Field(
        None,
        description="Specify if you want the invoice amount calculated with a specific "
        "currency symbol",
    )
    callback_url: str | None = Field(
        None,
        description="The URL where payment information will be sent",
        serialization_alias="callbackUrl",
    )
    under_paid_cover: float | None = Field(
        None,
        ge=0,
        le=60,
        description="Acceptable inaccuracy in payment (0-60.00)",
        serialization_alias="underPaidCover",
    )
    fee_paid_by_payer: int | None = Field(
        None,
        ge=0,
        le=1,
        description="Whether payer covers invoice commission (1) or merchant does (0)",
        serialization_alias="feePaidByPayer",
    )
    life_time: int | None = Field(
        None,
        ge=15,
        le=2880,
        description="Expiration time for payment link in minutes (15-2880)",
        serialization_alias="lifeTime",
    )
    email: str | None = Field(
        None,
        description="Payer's email address for reporting",
    )
    order_id: str | None = Field(
        None,
        description="Unique order ID for reference",
        serialization_alias="orderId",
    )
    description: str | None = Field(
        None,
        description="Order details or additional information",
    )
    return_url: str | None = Field(
        None,
        description="URL for redirecting payer after successful payment",
        serialization_alias="returnUrl",
    )


class CreateInvoiceResponse(ResultResponse):
    """Response model for invoice creation."""

    track_id: str = Field(
        ...,
        description="Unique identifier for the payment session",
        validation_alias="trackId",
    )
    pay_link: str = Field(
        ...,
        description="Payment page link for the payer",
        validation_alias="payLink",
    )


# White-label payment
class CreateWhiteLabelRequest(BaseModel):
    """Request model for creating a white-label payment."""

    amount: int | float = Field(..., description="The amount for the payment")
    pay_currency: str = Field(
        ...,
        description="Specific currency for payment",
        serialization_alias="payCurrency",
    )
    currency: str | None = Field(
        None,
        description="Specify if you want the invoice amount calculated with a specific "
        "currency symbol",
    )
    network: str | None = Field(
        None,
        description="Blockchain network for the payment",
    )
    email: str | None = Field(None, description="Payer's email address")
    order_id: str | None = Field(
        None,
        description="Unique order ID for reference",
        serialization_alias="orderId",
    )
    description: str | None = Field(None, description="Additional information")
    callback_url: str | None = Field(
        None,
        description="URL for payment notifications",
        serialization_alias="callbackUrl",
    )
    under_paid_cover: float | None = Field(
        None,
        ge=0,
        le=60,
        description="Acceptable inaccuracy in payment (0-60.00)",
        serialization_alias="underPaidCover",
    )
    fee_paid_by_payer: int | None = Field(
        None,
        ge=0,
        le=1,
        description="Whether payer covers invoice commission (1) or merchant does (0)",
        serialization_alias="feePaidByPayer",
    )
    life_time: int | None = Field(
        None,
        ge=15,
        le=2880,
        description="Expiration time in minutes (15-2880)",
        serialization_alias="lifeTime",
    )


class CreateWhiteLabelResponse(ResultResponse):
    """Response model for white-label payment creation."""

    track_id: str = Field(
        ...,
        description="Unique identifier for the payment session",
        validation_alias="trackId",
    )
    amount: int | float = Field(..., description="Requested payment amount")
    currency: str = Field(..., description="Requested payment currency")
    pay_amount: int | float = Field(
        ...,
        description="Actual payment amount",
        validation_alias="payAmount",
    )
    pay_currency: str = Field(
        ...,
        description="Actual payment currency",
        validation_alias="payCurrency",
    )
    network: str = Field(..., description="Blockchain network")
    address: str = Field(..., description="Generated cryptocurrency address")
    callback_url: str | None = Field(
        None,
        description="Callback URL",
        validation_alias="callbackUrl",
    )
    description: str | None = Field(None, description="Description")
    email: str | None = Field(None, description="Email")
    fee_paid_by_payer: float = Field(
        ...,
        description="Fee paid by payer setting",
        validation_alias="feePaidByPayer",
    )
    life_time: int = Field(
        ...,
        description="Payment lifetime",
        validation_alias="lifeTime",
    )
    order_id: str | None = Field(
        None,
        description="Order ID",
        validation_alias="orderId",
    )
    under_paid_cover: float = Field(
        ...,
        description="Underpaid cover setting",
        validation_alias="underPaidCover",
    )
    rate: float = Field(..., description="Exchange rate")
    expired_at: str = Field(
        ...,
        description="Expiration time",
        validation_alias="expiredAt",
    )
    created_at: str = Field(
        ...,
        description="Creation time",
        validation_alias="createdAt",
    )
    qr_code: str = Field(
        ...,
        description="QR code image link",
        validation_alias="QRCode",
    )


# Static wallet
class CreateStaticWalletRequest(BaseModel):
    """Request model for creating a static wallet."""

    currency: str = Field(..., description="Currency for the static address")
    network: str | None = Field(None, description="Blockchain network")
    callback_url: str | None = Field(
        None,
        description="URL for payment notifications",
        serialization_alias="callbackUrl",
    )
    email: str | None = Field(None, description="Email address")
    order_id: str | None = Field(
        None,
        description="Order ID for reference",
        serialization_alias="orderId",
    )
    description: str | None = Field(None, description="Additional information")


class CreateStaticWalletResponse(ResultResponse):
    """Response model for static wallet creation."""

    address: str = Field(..., description="Generated static address")


class RevokeStaticWalletRequest(BaseModel):
    """Request model for revoking a static wallet."""

    address: str = Field(..., description="Address of the static wallet to revoke")


class RevokeStaticWalletResponse(ResultResponse):
    """Response model for static wallet revocation."""


class StaticWallet(BaseModel):
    """Model for static wallet information."""

    track_id: str = Field(
        ...,
        description="Unique identifier",
        serialization_alias="trackId",
    )
    address: str = Field(..., description="Static address")
    network: str = Field(..., description="Blockchain network")
    callback_url: str | None = Field(
        None,
        description="Callback URL",
        validation_alias="callbackUrl",
    )
    email: str | None = Field(None, description="Email")
    order_id: str | None = Field(
        None,
        description="Order ID",
        validation_alias="orderId",
    )
    description: str | None = Field(None, description="Description")
    date: str = Field(..., description="Creation timestamp")


class StaticWalletListRequest(BaseModel):
    """Request model for listing static wallets."""

    track_id: str | None = Field(
        None,
        description="Filter by specific invoice ID",
        serialization_alias="trackId",
    )
    page: int | None = Field(1, ge=1, description="Page number")
    size: int | None = Field(10, ge=1, le=200, description="Records per page")
    network: str | None = Field(None, description="Filter by blockchain network")
    address: str | None = Field(None, description="Filter by address")
    email: str | None = Field(None, description="Filter by email")
    order_id: str | None = Field(
        None,
        description="Filter by order ID",
        serialization_alias="orderId",
    )


class StaticWalletListResponse(ResultResponse):
    """Response model for listing static wallets."""

    data: list[StaticWallet] = Field(..., description="List of static wallets")
    meta: dict[str, int] = Field(..., description="Pagination metadata")


# Payment information
class PaymentInfoRequest(BaseModel):
    """Request model for getting payment information."""

    track_id: str = Field(
        ...,
        description="Unique identifier of the payment session",
        serialization_alias="trackId",
    )


class PaymentInfoResponse(ResultResponse):
    """Response model for payment information."""

    track_id: str = Field(
        ...,
        description="Unique identifier of the payment session",
        validation_alias="trackId",
    )
    status: PaymentStatus = Field(..., description="Current status of the payment")
    type: str = Field(..., description="Invoice type")
    amount: str = Field(..., description="Total payment amount")
    currency: str = Field(..., description="Payment currency")
    pay_amount: str = Field(
        ...,
        description="Actual amount paid",
        validation_alias="payAmount",
    )
    pay_currency: str = Field(
        ...,
        description="Currency in which payment was made",
        validation_alias="payCurrency",
    )
    network: str = Field(..., description="Blockchain network")
    address: str = Field(..., description="Payment address")
    tx_id: str | None = Field(
        None,
        description="Transaction ID",
        validation_alias="txID",
    )
    email: str | None = Field(None, description="Customer email")
    order_id: str | None = Field(
        None,
        description="Order ID",
        validation_alias="orderId",
    )
    description: str | None = Field(None, description="Description")
    fee_paid_by_payer: int = Field(
        ...,
        description="Fee paid by payer setting",
        validation_alias="feePaidByPayer",
    )
    under_paid_cover: int = Field(
        ...,
        description="Underpaid cover setting",
        validation_alias="underPaidCover",
    )
    date: str = Field(..., description="Creation time")
    pay_date: str | None = Field(
        None,
        description="Payment time",
        validation_alias="payDate",
    )


# Payment history
class PaymentHistoryRequest(BaseModel):
    """Request model for getting payment history."""

    order_by: OrderDirection | None = Field(
        OrderDirection.DESC,
        description="Sort order",
        serialization_alias="orderBy",
    )
    sort_by: SortField | None = Field(
        SortField.CREATE_DATE,
        description="Sort field",
        serialization_alias="sortBy",
    )
    track_id: str | None = Field(
        None,
        description="Filter by specific invoice ID",
        serialization_alias="trackId",
    )
    page: int | None = Field(1, ge=1, description="Page number")
    size: int | None = Field(10, ge=1, le=200, description="Records per page")
    order_id: str | None = Field(
        None,
        description="Filter by order ID",
        serialization_alias="orderId",
    )
    status: PaymentStatus | None = Field(None, description="Filter by status")
    fee_paid_by_payer: int | None = Field(
        None,
        ge=0,
        le=1,
        description="Filter by fee paid setting",
        serialization_alias="feePaidByPayer",
    )
    type: PaymentType | None = Field(None, description="Filter by payment type")
    network: str | None = Field(None, description="Filter by blockchain network")
    pay_currency: str | None = Field(
        None,
        description="Filter by payment currency",
        serialization_alias="payCurrency",
    )
    currency: str | None = Field(None, description="Filter by currency")
    to_amount: float | None = Field(
        None,
        description="Filter by maximum amount",
        serialization_alias="toAmount",
    )
    from_amount: float | None = Field(
        None,
        description="Filter by minimum amount",
        serialization_alias="fromAmount",
    )
    to_date: int | str | None = Field(
        None,
        description="End date for filtering (unix timestamp)",
        serialization_alias="toDate",
    )
    from_date: int | str | None = Field(
        None,
        description="Start date for filtering (unix timestamp)",
        serialization_alias="fromDate",
    )
    address: str | None = Field(None, description="Filter by address")
    tx_id: str | None = Field(
        None,
        description="Filter by transaction hash",
        serialization_alias="txID",
    )


class Payment(BaseModel):
    """Model for payment information in history."""

    track_id: str = Field(
        ...,
        description="Unique identifier",
        validation_alias="trackId",
    )
    status: PaymentStatus = Field(..., description="Payment status")
    type: str = Field(..., description="Payment type")
    amount: str = Field(..., description="Payment amount")
    currency: str = Field(..., description="Currency")
    pay_amount: str | None = Field(
        None,
        description="Actual amount paid",
        validation_alias="payAmount",
    )
    pay_currency: str | None = Field(
        None,
        description="Payment currency",
        validation_alias="payCurrency",
    )
    network: str | None = Field(None, description="Blockchain network")
    address: str | None = Field(None, description="Payment address")
    tx_id: str | None = Field(
        None,
        description="Transaction ID",
        validation_alias="txID",
    )
    email: str | None = Field(None, description="Email")
    order_id: str | None = Field(
        None,
        description="Order ID",
        validation_alias="orderId",
    )
    description: str | None = Field(None, description="Description")
    date: str = Field(..., description="Creation timestamp")
    pay_date: str | None = Field(
        None,
        description="Payment timestamp",
        validation_alias="payDate",
    )


class PaymentHistoryResponse(PaginatedResponse[Payment]):
    """Response model for payment history."""


# Accepted coins
class AcceptedCoinsRequest(BaseModel):
    """Request model for getting accepted coins."""


class AcceptedCoinsResponse(ResultResponse):
    """Response model for accepted coins."""

    allowed: list[str] = Field(..., description="List of accepted cryptocurrencies")
