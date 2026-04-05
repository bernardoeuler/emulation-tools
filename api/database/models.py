from typing import List
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    func,
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class DownloadStatusEnum(str, Enum):
    PENDING = "pending"
    READY = "ready"
    EXPIRED = "expired"
    FAILED = "failed"


class RequestStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"


class RequestTypeEnum(str, Enum):
    ROM_CONVERSION = "rom_conversion"


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Download(Base):
    __tablename__ = "downloads"

    public_id: Mapped[str] = mapped_column(String(32), nullable=False)
    request_id: Mapped[int] = mapped_column(Integer, ForeignKey("requests.id"), nullable=False)
    status: Mapped[DownloadStatusEnum] = mapped_column(SQLEnum(DownloadStatusEnum, name="download_status_enum"), nullable=False)
    file_uri: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    request: Mapped["Request"] = relationship("Request", back_populates="downloads")


class Request(Base):
    __tablename__ = "requests"

    public_id: Mapped[str] = mapped_column(String(32), nullable=False)
    type: Mapped[RequestTypeEnum] = mapped_column(SQLEnum(RequestTypeEnum, name="request_type_enum"), nullable=False)
    status: Mapped[RequestStatusEnum] = mapped_column(SQLEnum(RequestStatusEnum, name="request_status_enum"), nullable=False)

    downloads: Mapped[List["Download"]] = relationship("Download", back_populates="request")
