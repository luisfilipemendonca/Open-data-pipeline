from typing import Annotated

from fastapi import Query

from open_data_pipeline.api.schemas import PaginationParams

DEFAULT_PAGE_SIZE = 10


def get_pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = DEFAULT_PAGE_SIZE,
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)
