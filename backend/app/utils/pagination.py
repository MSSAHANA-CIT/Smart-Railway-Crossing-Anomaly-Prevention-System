"""Reusable pagination helpers and response envelope."""

from math import ceil
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

T = TypeVar("T")

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


class PaginationParams(BaseModel):
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    page_size: int = Field(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


def pagination_params(
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number (1-based)"),
    page_size: int = Query(
        DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description=f"Items per page (max {MAX_PAGE_SIZE})",
    ),
) -> PaginationParams:
    """FastAPI dependency for page/page_size query parameters."""
    return PaginationParams(page=page, page_size=page_size)


def build_paginated_response(
    items: list[T],
    *,
    total: int,
    page: int,
    page_size: int,
) -> PaginatedResponse[T]:
    """Build a standard paginated response envelope."""
    total_pages = ceil(total / page_size) if page_size > 0 and total > 0 else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
