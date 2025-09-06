from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(32), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    file_uri = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    request = relationship("Request", back_populates="downloads")

class Request(Base):
    __tablename__ = "requests"
    __table_args__ = (
        CheckConstraint("status IN ('pending','processing','done','failed')", name="status_check"),
    )

    id = Column(Integer, primary_key=True)
    public_id = Column(String(32), nullable=False)
    type_id = Column(Integer, ForeignKey("request_types.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    type = relationship("RequestType", back_populates="requests")
    downloads = relationship("Download", back_populates="request")

class RequestType(Base):
    __tablename__ = "request_types"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    description = Column(String)

    requests = relationship("Request", back_populates="type")