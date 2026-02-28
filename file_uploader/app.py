import logging

from fastapi import APIRouter, FastAPI

from file_uploader.settings import Settings

logging.basicConfig(level=logging.INFO)
settings = Settings()

app = FastAPI()
v1_apirouter = APIRouter(prefix='/v1')
# v1_apirouter.include_router(YOUR_ROUTER)
app.include_router(v1_apirouter)


@app.get('/health')
def health_check():
    return {'version': settings.version, 'message': 'ok'}
