from sqlalchemy import (
    Column,
    Integer,
    String,
    CheckConstraint,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from config.database.base_model import BaseModel


class Request(BaseModel):
    __tablename__ = "requests"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','in_progress','done','failed')", name="status_check"
        ),
    )

    public_id = Column(String(32), nullable=False)
    type_id = Column(Integer, ForeignKey("request_types.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    type = relationship("RequestType", back_populates="requests")
    downloads = relationship("Download", back_populates="request")
