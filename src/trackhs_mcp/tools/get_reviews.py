"""
Herramienta MCP para obtener reseñas de Track HS
"""

from typing import Optional, Literal
from .core.api_client import TrackHSApiClient
from ..types import ReviewsResponse, GetReviewsParams

async def get_reviews(
    page: int = 1,
    size: int = 10,
    sort_column: Literal["id"] = "id",
    sort_direction: Literal["asc", "desc"] = "asc",
    search: Optional[str] = None,
    updated_since: Optional[str] = None
) -> ReviewsResponse:
    """
    Retrieve paginated collection of property reviews from Track HS
    
    Args:
        page: Page Number (default: 1)
        size: Page Size (default: 10, max: 100)
        sort_column: Column to sort by
        sort_direction: Sort direction
        search: Search by reviewId and publicReview content
        updated_since: Filter reviews updated since this date (ISO 8601 format)
    
    Returns:
        ReviewsResponse: Paginated collection of reviews
    """
    # Esta función será implementada cuando se registre con el cliente API
    pass
