import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, JSONResponse
import requests
from loguru import logger
from typing import Dict, Optional, cast

from starlette.status import HTTP_404_NOT_FOUND


app = FastAPI()


class ErrorResponse(BaseModel):
    description: str


class MediaResponse(BaseModel):
    content_url: str
    content_type: str
    user: str
    description: str
    source_url: str


def format_error(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=code, content=ErrorResponse(description=message).model_dump()
    )


def validate_media_params(params: dict, url: str) -> Optional[JSONResponse]:
    for key, value in params.items():
        if value is None:
            logger.warning("Could not parse {key} from {url}", key=key, url=url)
            return format_error(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Could not construct a response. Most likely upstream has changed",
            )
    if len(list(params.keys())) != 5:
        return format_error(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Could not construct a response. Most likely upstream has changed",
        )
    return None


@app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get(
    "/insta/reel/{reel_id}",
    response_model=MediaResponse,
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def reel(reel_id: str) -> JSONResponse:
    url = f"https://kkinstagram.com/reel/{reel_id}"
    dd_response = requests.get(url, allow_redirects=False)
    if dd_response.status_code == 302:
        logger.info("HTTP 302 response from {url}", url=url)
        return format_error(
            code=status.HTTP_404_NOT_FOUND,
            message="Requested resource most likely does not exist",
        )
    if dd_response.status_code != 200:
        logger.info("Non 200 response from url {url}", url=url)
        return format_error(
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"Upstream service respnded with HTTP {dd_response.status_code}.",
        )

    html = dd_response.text
    root = ET.fromstring(html)

    head_element = root.find("head")
    if head_element is None:
        logger.info("No head tag in response from {url}", url=url)
        return format_error(
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="Upstream responded with invalid HTML",
        )

    params = {}

    for meta in head_element.findall("meta"):
        prop = meta.get("property")
        if prop == "og:url":
            params["source_url"] = meta.get("content")
        if prop == "og:title":
            params["user"] = meta.get("content")
        if prop == "og:description":
            params["description"] = meta.get("content")
        if prop == "og:video:type":
            params["content_type"] = meta.get("content")
        if prop == "og:video":
            try:
                video_url = meta.get("content")
                if video_url is None:
                    raise ValueError("No video url")
                video_url = (
                    f"https://ddinstagram.com{video_url}"
                    if video_url[0] == "/"
                    else video_url
                )
                video_response = requests.get(video_url, allow_redirects=False)
                params["content_url"] = video_response.headers["Location"]
            except Exception:
                logger.exception("could not get content_url for {url}", url=url)
                return format_error(
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Could not get video url",
                )

    err = validate_media_params(params=params, url=url)
    if err is not None:
        return err

    resp = MediaResponse(**cast(Dict[str, str], params))
    return JSONResponse(status_code=200, content=resp.model_dump())


@app.get(
    "/x/status/{status_id}",
    response_model=MediaResponse,
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def x_status(status_id: int) -> JSONResponse:
    url = f"https://api.vxtwitter.com/status/{status_id}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.info(
            "Non 200 response ({code}) from url {url}",
            code=response.status_code,
            url=url,
        )
        return format_error(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Upstream service respnded with HTTP {response.status_code}.",
        )

    body = response.json()

    params = {}

    for meta in head_element.findall("meta"):
        prop = meta.get("property")
        content = meta.get("content")
        if prop == "og:url":
            params["source_url"] = content
        if prop == "og:title":
            params["user"] = content
        if prop == "og:description":
            params["description"] = content
        if prop == "og:video:type":
            params["content_type"] = content
        if prop == "og:video":
            params["content_url"] = content

    # Search for images only if no videos were found
    if "content_url" not in params:
        for meta in head_element.findall("meta"):
            prop = meta.get("property")
            content = meta.get("content")
            if prop == "og:image":
                params["content_url"] = content
                content_url = (content or "").lower()
                if ".png" in content_url:
                    params["content_type"] = "image/png"
                elif "jpeg" in content_url or "jpg" in content_url:
                    params["content_type"] = "image/jpeg"
                else:
                    params["content_type"] = "image/unknown"

    if len(params) == 1 and "description" in params:
        logger.info("Could not find content from {url}", url=url)
        return format_error(
            code=status.HTTP_404_NOT_FOUND,
            message=params.get("description") or "Content most likely does not exist",
        )

    err = validate_media_params(params=params, url=url)
    if err is not None:
        return err

    resp = MediaResponse(**cast(Dict[str, str], params))
    return JSONResponse(status_code=200, content=resp.model_dump())
