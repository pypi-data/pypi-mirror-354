"""Models for OxaPay Payout API."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from .base import OrderDirection, PaginatedResponse, ResultResponse, SortField


class PayoutStatus(str, Enum):
    """Payout status enum."""

    PROCESSING = "Processing"
    CONFIRMING = "Confirming"
    COMPLETE = "Complete"
    REJECTED = "Rejected"


class PayoutType(str, Enum):
    """Payout type enum."""

    INTERNAL = "internal"
    EXTERNAL = "external"


class CreatePayoutRequest(BaseModel):
    """Request model for creating a payout."""

    address: str = Field(..., description="Cryptocurrency address of the recipient")
    amount: float = Field(..., description="Amount of cryptocurrency to send")
    currency: str = Field(..., description="Cryptocurrency symbol")
    network: str | None = Field(None, description="Blockchain network")
    memo: str | None = Field(None, description="Memo for networks that support it")
    callback_url: str | None = Field(
        None,
        description="URL for payout notifications",
        serialization_alias="callbackUrl",
    )
    description: str | None = Field(None, description="Additional information")


class CreatePayoutResponse(ResultResponse):
    """Response model for payout creation."""

    track_id: str = Field(
        ...,
        description="Unique identifier for the payout",
        validation_alias="trackId",
    )
    status: PayoutStatus = Field(..., description="Current status of the payout")


class PayoutInfoRequest(BaseModel):
    """Request model for getting payout information."""

    track_id: str = Field(
        ...,
        description="Unique identifier of the payout",
        serialization_alias="trackId",
    )


class PayoutInfoResponse(ResultResponse):
    """Response model for payout information."""

    track_id: str = Field(
        ...,
        description="Unique identifier",
        validation_alias="trackId",
    )
    address: str = Field(..., description="Recipient's address")
    currency: str = Field(..., description="Cryptocurrency symbol")
    network: str = Field(..., description="Blockchain network")
    amount: str = Field(..., description="Payout amount")
    fee: str = Field(..., description="Transaction fee")
    status: PayoutStatus = Field(..., description="Current status")
    type: PayoutType = Field(..., description="Payout type")
    tx_id: str | None = Field(
        None,
        description="Transaction ID",
        validation_alias="txID",
    )
    date: str = Field(..., description="Creation timestamp")
    description: str | None = Field(None, description="Description")


class PayoutHistoryRequest(BaseModel):
    """Request model for getting payout history."""

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
    page: int | None = Field(1, ge=1, description="Page number")
    size: int | None = Field(10, ge=1, le=200, description="Records per page")
    status: PayoutStatus | None = Field(None, description="Filter by status")
    type: PayoutType | None = Field(None, description="Filter by type")
    network: str | None = Field(None, description="Filter by network")
    currency: str | None = Field(None, description="Filter by currency")
    to_amount: str | None = Field(
        None,
        description="Maximum amount",
        serialization_alias="toAmount",
    )
    from_amount: str | None = Field(
        None,
        description="Minimum amount",
        serialization_alias="fromAmount",
    )
    to_date: datetime | None = Field(
        None,
        description="End date",
        serialization_alias="toDate",
    )
    from_date: datetime | None = Field(
        None,
        description="Start date",
        serialization_alias="fromDate",
    )


class Payout(BaseModel):
    """Model for payout information in history."""

    id: str = Field(..., description="Unique identifier")
    address: str = Field(..., description="Recipient's address")
    currency: str = Field(..., description="Cryptocurrency symbol")
    network: str = Field(..., description="Blockchain network")
    amount: str = Field(..., description="Payout amount")
    fee: str = Field(..., description="Transaction fee")
    status: PayoutStatus = Field(..., description="Current status")
    type: PayoutType = Field(..., description="Payout type")
    tx_id: str | None = Field(
        None,
        description="Transaction ID",
        validation_alias="txID",
    )
    date: datetime = Field(..., description="Creation timestamp")
    description: str | None = Field(None, description="Description")


class PayoutHistoryResponse(PaginatedResponse[Payout]):
    """Response model for payout history."""
