from typing import Optional

from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    __name__: str

    @staticmethod
    def camel_to_snake(s):
        return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.camel_to_snake(cls.__name__)

    class Config:
        orm_mode = True
