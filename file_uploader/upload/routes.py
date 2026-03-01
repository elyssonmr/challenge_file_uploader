import logging
from http import HTTPStatus
from pathlib import Path
from typing import Annotated
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.database import get_session
from file_uploader.models import ZipUpload
from file_uploader.schemas import ZipUploadResponse
from file_uploader.settings import Settings

# from file_uploader.schemas import ASCHEMA
# from file_uploader.services import ASERVICE

settings = Settings()

logger = logging.getLogger()

T_Session = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix='/upload', tags=['File Upload'])


UPLOAD_FOLDER = Path(settings.UPLOAD_FOLDER)
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post('/zip', status_code=HTTPStatus.OK)
async def upload_zip_file(file: UploadFile, session: T_Session):
    if file.content_type not in {
        'application/x-zip-compressed',
        'application/x-zip',
        'application/zip',
    }:
        raise HTTPException(
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE.description,
        )

    # Save uploaded file
    safe_name = Path(file.filename).name
    identification = str(uuid4())
    target_path = UPLOAD_FOLDER / identification

    try:
        async with aiofiles.open(target_path, 'wb') as output_file:
            while chunk := await file.read(settings.BUFFER_SIZE):
                await output_file.write(chunk)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            'There was an error processing the uploaded file',
        )
    finally:
        await file.close()

    # save to database
    zip_upload = ZipUpload(
        file_name=safe_name,
        upload_identification=identification,
    )
    try:
        session.add(zip_upload)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='File with the same name is already uploaded',
        )

    return ZipUploadResponse(file_identification=identification)
