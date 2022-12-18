import uuid

from fastapi import APIRouter, status, HTTPException, Depends
import utils
from schamas import Delivery


delivery_router = APIRouter(
    tags=['Delivery'],
    prefix='/delivery',
)


@delivery_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[Delivery],
)
@utils.trace_it(tag='get all deliveries', value='Get method')
async def get_all_deliveries():
    return utils.deliveries


@delivery_router.get(
    '/{user_uuid}}',
    status_code=status.HTTP_200_OK,
    response_model=list[Delivery],
)
@utils.trace_it(tag='get delivery by user_uuid', value='Get method')
async def create_delivery(user_uuid: uuid.UUID):
    return list(filter(lambda x: x.user_uuid == user_uuid, utils.deliveries))
