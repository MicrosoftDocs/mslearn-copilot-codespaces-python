from fastapi import APIRouter, Depends

from webapp.dependencies import get_token_service
from webapp.models import Body
from webapp.services.token_service import TokenService

router = APIRouter()


@router.post('/generate')
def generate(body: Body, service: TokenService = Depends(get_token_service)):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    return {'token': service.generate(body.length)}
