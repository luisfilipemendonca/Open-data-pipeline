from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from open_data_pipeline.api.pagination import get_pagination
from open_data_pipeline.api.schemas import PaginationParams
from open_data_pipeline.db.session import get_db

DbDep = Annotated[Session, Depends(get_db)]
PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]
