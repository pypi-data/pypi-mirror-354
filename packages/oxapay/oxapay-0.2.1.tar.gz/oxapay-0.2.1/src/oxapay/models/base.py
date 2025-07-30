"""Base models for OxaPay API."""

from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")


def timestamp_to_datetime(value: int | str | None) -> datetime | None:
    """Convert a Unix timestamp to a datetime object."""
    if value is None:
        return None
    # Convert string to int if needed
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    # Handle timestamp as int
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value)  # noqa: DTZ006
    return value  # Return as is if already a datetime or incompatible format


class TimestampModelMixin:
    """Mixin for models with timestamp fields."""

    @model_validator(mode="before")
    @classmethod
    def convert_timestamps(cls, data: Any) -> Any:  # noqa: ANN401
        """Convert all timestamp fields to datetime objects."""
        if not isinstance(data, dict):
            return data

        # Standard timestamp field names to convert
        timestamp_fields = ["date", "payDate", "createdAt", "expiredAt"]

        # Process known timestamp fields
        for field in timestamp_fields:
            if field in data and data[field] is not None:
                data[field] = timestamp_to_datetime(data[field])

        # Process fields ending with 'Date' or 'At'
        for field in list(data.keys()):
            if (
                (field.endswith(("Date", "At")))
                and field not in timestamp_fields
                and data[field] is not None
            ):
                data[field] = timestamp_to_datetime(data[field])

        return data


class ResultResponse(BaseModel):
    """Base response with result code and message."""

    result: int = Field(
        ...,
        description="The result code indicates the success or failure of the request",
    )
    message: str = Field(
        ...,
        description="A message providing additional information about the result",
    )


class PaginatedResponse(ResultResponse, Generic[T]):
    """Base model for paginated responses."""

    data: list[T] = Field(..., description="The paginated data")
    meta: dict[str, int] = Field(
        ...,
        description="Pagination metadata (size, page, pages, total)",
    )


class OrderDirection(str, Enum):
    """Order direction for listings."""

    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    """Sort field options for listings."""

    CREATE_DATE = "create_date"
    PAY_DATE = "pay_date"
    AMOUNT = "amount"
