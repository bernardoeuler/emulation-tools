from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from config.database.base_model import BaseModel


class RequestType(BaseModel):
    __tablename__ = "request_types"

    code = Column(String, unique=True, nullable=False)
    description = Column(String)

    requests = relationship("Request", back_populates="type")
