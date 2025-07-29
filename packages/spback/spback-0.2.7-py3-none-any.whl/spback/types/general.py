import typing as t

from ninja_extra.router import Router
from pydantic import BaseModel
from typing import Optional
# from ninja import Schema


class ResponseModel(BaseModel):
  success: bool
  data: t.Optional[dict]
  errorMessage: Optional[str]


class PagedData(t.TypedDict):
  current_page: int
  offset: int  # number in one page
  page_range: t.Tuple[int, int]  # start, end
  data: t.List[dict]


url = str
RouterGroup = t.Tuple[url, Router]
