import logging
from http import HTTPStatus

from fastapi import APIRouter

# from file_uploader.schemas import ASCHEMA
# from file_uploader.services import ASERVICE

logger = logging.getLogger()

router = APIRouter(prefix='/YOUR_PREFIX', tags=['SWAGGER PREFIX'])


@router.post('/YOUR_URL', status_code=HTTPStatus.CREATED)
async def endpoint_name():
    # Here goes the endpoint code
    pass
