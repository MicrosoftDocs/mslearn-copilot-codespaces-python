from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    items: list[str]
    total: int
    page: int
    page_size: int
    total_pages: int
