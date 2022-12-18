from pydantic import BaseModel
from uuid import UUID


class BaseDelivery(BaseModel):
    name: str
    user_uuid: UUID


class Delivery(BaseDelivery):
    id: int
