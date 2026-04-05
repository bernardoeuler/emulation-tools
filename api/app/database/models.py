from sqlalchemy import (
    Column,
    Integer,
    String,
    CheckConstraint,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)


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


class RequestType(BaseModel):
    __tablename__ = "request_types"

    code = Column(String, unique=True, nullable=False)
    description = Column(String)

    requests = relationship("Request", back_populates="type")
