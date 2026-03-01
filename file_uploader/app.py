import logging

from fastapi import APIRouter, FastAPI

from file_uploader.settings import Settings
from file_uploader.upload.routes import router as upload_router

logging.basicConfig(level=logging.INFO)
settings = Settings()

app = FastAPI()
v1_apirouter = APIRouter(prefix='/v1')
v1_apirouter.include_router(upload_router)
app.include_router(v1_apirouter)


@app.get('/health')
def health_check():
    return {'version': settings.VERSION, 'message': 'ok'}
