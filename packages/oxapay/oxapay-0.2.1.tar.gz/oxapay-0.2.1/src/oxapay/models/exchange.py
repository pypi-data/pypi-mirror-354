"""Models for OxaPay Exchange API."""

from enum import Enum

from pydantic import BaseModel, Field

from .base import OrderDirection, PaginatedResponse, ResultResponse, SortField


class ExchangeType(str, Enum):
    """Exchange type enum."""

    AUTO_CONVERT = "autoConvert"
    MANUAL_SWAP = "manualSwap"
    SWAP_BY_API = "swapByApi"


class ExchangePair(BaseModel):
    """Model for exchange pair information."""

    from_currency: str = Field(
        ...,
        validation_alias="fromCurrency",
        description="Source currency symbol",
    )
    to_currency: str = Field(
        ...,
        validation_alias="toCurrency",
        description="Target currency symbol",
    )
    min_amount: str = Field(
        ...,
        validation_alias="minAmount",
        description="Minimum conversion amount",
    )


class ExchangeRateRequest(BaseModel):
    """Request model for exchange rate."""

    from_currency: str = Field(
        ...,
        validation_alias="fromCurrency",
        description="Source currency symbol",
    )
    to_currency: str = Field(
        ...,
        validation_alias="toCurrency",
        description="Target currency symbol",
    )


class ExchangeRateResponse(ResultResponse):
    """Response model for exchange rate."""

    rate: str = Field(..., description="Exchange rate")


class ExchangeCalculateRequest(BaseModel):
    """Request model for exchange calculation."""

    from_currency: str = Field(
        ...,
        serialization_alias="fromCurrency",
        description="Source currency symbol",
    )
    to_currency: str = Field(
        ...,
        serialization_alias="toCurrency",
        description="Target currency symbol",
    )
    amount: float = Field(..., description="Amount to convert")


class ExchangeCalculateResponse(ResultResponse):
    """Response model for exchange calculation."""

    rate: str = Field(..., description="Exchange rate")
    amount: str = Field(..., description="Input amount")
    to_amount: str = Field(
        ...,
        validation_alias="toAmount",
        description="Resulting amount",
    )


class ExchangePairsResponse(ResultResponse):
    """Response model for exchange pairs."""

    pairs: list[ExchangePair] = Field(..., description="Available exchange pairs")


class ExchangeRequestRequest(BaseModel):
    """Request model for exchange request."""

    from_currency: str = Field(
        ...,
        serialization_alias="fromCurrency",
        description="Source currency symbol",
    )
    to_currency: str = Field(
        ...,
        serialization_alias="toCurrency",
        description="Target currency symbol",
    )
    amount: float = Field(..., description="Amount to convert")


class ExchangeRequestResponse(ResultResponse):
    """Response model for exchange request."""

    track_id: str = Field(
        ...,
        validation_alias="trackId",
        description="Exchange transaction ID",
    )
    status: str = Field(..., description="Exchange status")
    amount: str = Field(..., description="Input amount")
    from_currency: str = Field(
        ...,
        validation_alias="fromCurrency",
        description="Source currency",
    )
    to_currency: str = Field(
        ...,
        validation_alias="toCurrency",
        description="Target currency",
    )
    to_amount: str = Field(
        ...,
        validation_alias="toAmount",
        description="Resulting amount",
    )
    rate: str = Field(..., description="Exchange rate")
    date: str = Field(..., description="Exchange timestamp")


class ExchangeHistoryRequest(BaseModel):
    """Request model for exchange history."""

    order_by: OrderDirection | None = Field(
        OrderDirection.DESC,
        serialization_alias="orderBy",
        description="Sort order",
    )
    sort_by: SortField | None = Field(
        SortField.CREATE_DATE,
        serialization_alias="sortBy",
        description="Sort field",
    )
    page: int | None = Field(1, ge=1, description="Page number")
    size: int | None = Field(10, ge=1, le=200, description="Records per page")
    type: ExchangeType | None = Field(None, description="Filter by exchange type")
    to_currency: str | None = Field(
        None,
        serialization_alias="toCurrency",
        description="Filter by target currency",
    )
    from_currency: str | None = Field(
        None,
        serialization_alias="fromCurrency",
        description="Filter by source currency",
    )
    to_date: int | str | None = Field(
        None,
        serialization_alias="toDate",
        description="End date (unix timestamp)",
    )
    from_date: int | str | None = Field(
        None,
        serialization_alias="fromDate",
        description="Start date (unix timestamp)",
    )
    track_id: int | None = Field(
        None,
        serialization_alias="trackId",
        description="Filter by transaction ID",
    )


class Exchange(BaseModel):
    """Model for exchange information in history."""

    track_id: str = Field(
        ...,
        validation_alias="trackId",
        description="Exchange transaction ID",
    )
    from_currency: str = Field(
        ...,
        validation_alias="fromCurrency",
        description="Source currency",
    )
    to_currency: str = Field(
        ...,
        validation_alias="toCurrency",
        description="Target currency",
    )
    from_amount: str = Field(
        ...,
        validation_alias="fromAmount",
        description="Input amount",
    )
    to_amount: str = Field(
        ...,
        validation_alias="toAmount",
        description="Resulting amount",
    )
    rate: str = Field(..., description="Exchange rate")
    type: ExchangeType = Field(..., description="Exchange type")
    date: str = Field(..., description="Exchange timestamp")


class ExchangeHistoryResponse(PaginatedResponse[Exchange]):
    """Response model for exchange history."""
