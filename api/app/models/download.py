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


class Download(BaseModel):
    __tablename__ = "downloads"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','ready','expired','failed')",
            name="download_status_check",
        ),
    )

    public_id = Column(String(32), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    status = Column(String, nullable=False)
    file_uri = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True))

    request = relationship("Request", back_populates="downloads")
