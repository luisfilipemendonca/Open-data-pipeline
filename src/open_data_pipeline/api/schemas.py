from pydantic import BaseModel


class PaginationResponse(BaseModel):
    page: int
    page_size: int
    total_pages: int
    has_next_page: bool
    total: int


class PaginatedResponse[T](BaseModel):
    data: list[T]
    pagination: PaginationResponse


class PaginationParams(BaseModel):
    page: int
    page_size: int
