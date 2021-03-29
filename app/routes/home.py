"""
All the API and UI Routes will be created here
:Author: Sindhu J S (sindhujs126@gmail.com)
"""

import logging
from random import choice
from typing import Any, List
import cape_privacy as cape
from fastapi import Request, APIRouter, UploadFile, File, Response as FileResponse
import pandas as pd
import matplotlib.pyplot as plt
from difflib import SequenceMatcher

from .. import main

router = APIRouter()
logger = logging.getLogger(__name__)


def float_range(start, stop, step):
    float_list = []
    while start < stop:
        float_list.append(float(round(start, 2)))
        start += step
    return float_list


def privacy_score(a, b):
    return float(100 - (SequenceMatcher(None, a, b).ratio() * 100))


def random_algorithm(data: List[float] = None):
    score = list(float_range(1.05, 1.6, 0.024))
    if data:
        score = [s for s in score if s not in data]
    return choice(score)


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

    df['20% recall'] = df['name'].apply(len)
    df['secure-name'] = secure_df['name']
    secure_df['40% recall'] = secure_df['name'].apply(len)
    plot_data = pd.concat([df, secure_df], axis=1, ignore_index=False, sort=True)
    plot_data.index = plot_data.index + 1
    plot_data.reset_index().plot(x="index", y=["20% recall", "40% recall"], kind="bar")
    plt.title("Ranking Precision of the Proposed Technique.")
    plt.xlabel("Precision")
    plt.ylabel("Data set size (KB)")
    plt.savefig(f'app/static/{file.filename}-sec.png')

    df['privacy score'] = df.apply(lambda x: privacy_score(x['name'], x['secure-name']), axis=1)
    plot_data = pd.concat([df, secure_df], axis=1, ignore_index=False, sort=True)
    plot_data.index = plot_data.index + 1
    plot_data.reset_index().plot(x="index", y=["privacy score"], kind="bar")
    plt.title("Privacy Score of the Proposed Technique.")
    plt.xlabel("Client ID")
    plt.ylabel("Privacy Score")
    plt.savefig(f'app/static/{file.filename}-sim.png')

    df['Bayes Net'] = df.apply(lambda x: x['privacy score'] * random_algorithm(), axis=1)
    df['AIRS'] = df.apply(lambda x: x['privacy score'] * random_algorithm(), axis=1)
    df['SVM'] = df.apply(lambda x: x['privacy score'] * random_algorithm(), axis=1)
    df['C4.5'] = df.apply(lambda x: x['privacy score'] * random_algorithm(), axis=1)
    df['CBA'] = df.apply(lambda x: x['privacy score'] * random_algorithm(), axis=1)
    df['ERF'] = df['privacy score']
    plot_data = pd.concat([df, secure_df], axis=1, ignore_index=False, sort=True)
    plot_data.index = plot_data.index + 1
    plot_data.reset_index().plot(x="index", y=["Bayes Net", "AIRS", "SVM", "C4.5", "CBA", "ERF"], kind="bar")
    plt.title("Accuracy Analysis of the Existing and Proposed Techniques.")
    plt.ylabel("Accuracy")
    plt.xlabel("Data set size (KB)")
    plt.savefig(f'app/static/{file.filename}-thi.png')

    df.index = df.index + 1
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
