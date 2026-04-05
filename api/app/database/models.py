from typing import List
from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    CheckConstraint,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Download(BaseModel):
    __tablename__ = "downloads"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','ready','expired','failed')",
            name="download_status_check",
        ),
    )

    public_id: Mapped[str] = mapped_column(String(32), nullable=False)
    request_id: Mapped[int] = mapped_column(Integer, ForeignKey("requests.id"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    file_uri: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    request: Mapped["Request"] = relationship("Request", back_populates="downloads")


class Request(BaseModel):
    __tablename__ = "requests"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','in_progress','done','failed')", name="status_check"
        ),
    )

    public_id: Mapped[str] = mapped_column(String(32), nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("request_types.id"), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    type: Mapped["RequestType"] = relationship("RequestType", back_populates="requests")
    downloads: Mapped[List["Download"]] = relationship("Download", back_populates="request")


class RequestType(BaseModel):
    __tablename__ = "request_types"

    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)

    requests: Mapped[List["Request"]] = relationship("Request", back_populates="type")
