"""
All the API and UI Routes will be created here
:Author: Sindhu J S (sindhujs126@gmail.com)
"""

import logging
from os import system
from typing import Any
import cape_privacy as cape
from fastapi import Request, APIRouter, UploadFile, File, Response as FileResponse, Form
import pandas as pd

from .. import main


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", tags=['Home'], response_model=Any, summary='Return the Basic HTML UI Page with basic Website',
            description='Retrieves the Basic HTML UI Page with basic Website', operation_id="home")
async def index(request: Request):
    """

    :param request:
    :return:
    """
    logger.info("Home Screen Rendered")
    return main.app.templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate_report", tags=['Home'], response_model=Any, summary='Return the Generated Report with basic Website',
             description='Retrieves the Generated Report with basic Website', operation_id="generate_report")
async def generate(request: Request, file: UploadFile = File(...), policy_file: UploadFile = File(...), download_data: Any = None):
    """
s
    :param file:
    :param policy_file:
    :param download_data:
    :param request:
    :return:
    """
    logger.info(f"Generate the code based Rendered data: {policy_file.filename} - {file.filename}")
    if file.filename.find('.csv') < 0:
        return main.app.templates.TemplateResponse("index.html", {"request": request, "error": "Please upload data only in CSV format...!!!"})
    if policy_file.filename.find('.yaml') < 0:
        return main.app.templates.TemplateResponse("index.html", {"request": request, "error": "Please upload Policy file only in yaml format...!!!"})

    df: pd.DataFrame = pd.read_csv(file.file)
    logger.info(df.head())
    with open(f"/tmp/{policy_file.filename}", 'wb+') as fd:
        fd.write(policy_file.file.read())
    policy = cape.parse_policy(f"/tmp/{policy_file.filename}")
    secure_df = cape.apply_policy(policy, df)
    logger.info(secure_df.head())
    system(f"rm -rf /tmp/{policy_file.filename}*")

    if download_data:
        return FileResponse(
            content=df.to_csv(), media_type='text/csv',
            headers={
                'content-disposition': f"attachment; filename=generate_data.csv",
                'content-type': 'text/csv'
            })

    return main.app.templates.TemplateResponse("index.html", {
        "request": request,
        "name": file.filename,
        "file": file,
        "data": df.to_html(),
        "secure_data": secure_df.to_html()
    })
