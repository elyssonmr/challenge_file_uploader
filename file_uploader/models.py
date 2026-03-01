from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy import JSON, ForeignKey, LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from file_uploader.settings import Settings

settings = Settings()
table_registry = registry()


def _now():
    return datetime.now(tz=ZoneInfo('UTC'))


class FileUploadStatus(StrEnum):
    TO_PROCESS = 'to_process'
    PROCESSING = 'processing'
    DONE = 'done'
    ERROR = 'error'


class BaseModel:
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=_now,
        nullable=False,
    )


@table_registry.mapped_as_dataclass
class ZipUpload(BaseModel):
    __tablename__ = 'file_uploads'

    file_name: Mapped[str] = mapped_column(String(150), unique=True)
    upload_identification: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(
        String(20), default=FileUploadStatus.TO_PROCESS, init=False
    )
    articles_count: Mapped[int] = mapped_column(init=False, default=0)
    error_reason: Mapped[str] = mapped_column(init=False, nullable=True)
    extracted_articles: Mapped[list['ArticleEntry']] = relationship(
        back_populates='from_uploaded_zip', init=False
    )

    @property
    def upload_path(self):
        uploads_folder = Path(settings.upload_folder)
        return uploads_folder / self.upload_identification


@table_registry.mapped_as_dataclass
class ArticleEntry(BaseModel):
    __tablename__ = 'article_entries'

    file: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    data_processed: Mapped[datetime] = mapped_column(
        default=_now, index=True, init=False
    )
    article_metadata: Mapped[dict[str, Any]] = mapped_column(JSON())
    from_uploaded_zip_fk: Mapped[int] = mapped_column(
        ForeignKey('file_uploads.id')
    )
    from_uploaded_zip: Mapped[ZipUpload] = relationship(
        back_populates='extracted_articles', init=False
    )
