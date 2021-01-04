"""
Data Cap Privacy Tools project will generate few reports related to data privacy
:Author: Sindhu J S (sindhujs126@gmail.com)
"""
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .core.log import setup_logging
from .core.settings import AppSettings, get_settings
from .routes import home


api_prefix: str = '/api/v1'
config: AppSettings = get_settings()

setup_logging(config)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Data Cap Privacy",
    version="0.1.0",
    description="Data Cap Privacy Tools project will generate few reports related to data privacy",
    openapi_url='/api/v1/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./app/static"), name='static')
app.templates = Jinja2Templates(directory='./app/templates')


@app.on_event('startup')
async def startup():
    logger.info('Setting up application resources')
    logger.info('Application startup complete')


@app.on_event('shutdown')
async def shutdown():
    logger.info('Cleaning up application resources')
    logger.info('Application Shutdown completed')


# All the UI and Website Routes goes below
app.include_router(home.router)
