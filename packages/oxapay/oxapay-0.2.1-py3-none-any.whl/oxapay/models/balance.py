"""Models for OxaPay Balance API."""

from pydantic import BaseModel, Field

from .base import ResultResponse


class AccountBalanceRequest(BaseModel):
    """Request model for account balance."""

    currency: str | None = Field(
        None,
        description="Specific currency to get balance for",
    )


class AccountBalanceResponse(ResultResponse):
    """Response model for account balance."""

    data: dict[str, str] = Field(..., description="Balances for each currency")
