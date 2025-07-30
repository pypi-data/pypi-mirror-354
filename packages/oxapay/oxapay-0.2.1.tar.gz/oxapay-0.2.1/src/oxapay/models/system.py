"""Models for OxaPay System API."""

from typing import Any

from pydantic import BaseModel, Field

from .base import ResultResponse


class NetworkInfo(BaseModel):
    """Model for network information."""

    network: str = Field(..., description="Network identifier")
    name: str = Field(..., description="Network name")
    min_confirm: int = Field(
        ...,
        description="Minimum confirmations required",
        validation_alias="minConfirm",
    )
    withdraw_fee: float = Field(
        ...,
        description="Withdrawal fee",
        validation_alias="withdrawFee",
    )
    withdraw_min: float = Field(
        ...,
        description="Minimum withdrawal amount",
        validation_alias="withdrawMin",
    )
    deposit_min: float = Field(
        ...,
        description="Minimum deposit amount",
        validation_alias="depositMin",
    )
    static_fixed_fee: float = Field(
        ...,
        description="Static fixed fee",
        validation_alias="staticFixedFee",
    )


class CurrencyInfo(BaseModel):
    """Model for currency information."""

    symbol: str = Field(..., description="Currency symbol")
    name: str = Field(..., description="Currency name")
    status: bool = Field(..., description="Currency status")
    network_list: dict[str, NetworkInfo] = Field(
        ...,
        description="Available networks",
        validation_alias="networkList",
    )


class SupportedCurrenciesResponse(ResultResponse):
    """Response model for supported currencies."""

    data: dict[str, CurrencyInfo] = Field(
        ...,
        description="Supported currencies information",
    )


class FiatCurrencyInfo(BaseModel):
    """Model for fiat currency information."""

    symbol: str = Field(..., description="Currency symbol")
    name: str = Field(..., description="Currency name")
    price: str = Field(..., description="Current price")
    display_precision: str = Field(
        ...,
        description="Display precision",
        validation_alias="displayPrecision",
    )


class SupportedFiatCurrenciesResponse(ResultResponse):
    """Response model for supported fiat currencies."""

    data: dict[str, FiatCurrencyInfo] = Field(
        ...,
        description="Supported fiat currencies information",
    )


class SupportedNetworksResponse(ResultResponse):
    """Response model for supported networks."""

    data: list[str] = Field(..., description="List of supported network names")


class PriceResponse(ResultResponse):
    """Response model for cryptocurrency prices."""

    data: dict[str, Any] = Field(
        ...,
        description="Current prices of supported cryptocurrencies",
    )
