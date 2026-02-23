from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    """Response model for a paginated list of generated tokens.

    Attributes:
        items: The tokens generated for the requested page.
        total: The server-side maximum number of tokens (cap).
        page: The current 1-indexed page number.
        page_size: The number of tokens requested per page.
        total_pages: Total number of pages given ``total`` and ``page_size``.
    """

    items: list[str]
    total: int
    page: int
    page_size: int
    total_pages: int
