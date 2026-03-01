from uuid import UUID

from pydantic import BaseModel


class ZipUploadResponse(BaseModel):
    file_identification: UUID
