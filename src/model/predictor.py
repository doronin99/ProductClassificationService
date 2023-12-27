from sqlmodel import Field

from src.model.base_model import BaseModel


class Predictor(BaseModel, table=False):
    name: str = Field(unique=True)
    cost: int = Field()
    is_active: bool = Field(default=True)
