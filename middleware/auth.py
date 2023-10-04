from fastapi import Request, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import base64
from utils.exceptions import CredentialsException
from dotenv import load_dotenv
import os
from __init__ import __title__, __version__

load_dotenv()

PROTECTED_ENDPOINTS = ("/alerts")
security = HTTPBasic()


async def apply_basic_auth(request: Request, call_next):
    try:
        if request.url.path.startswith(PROTECTED_ENDPOINTS):
            auth_header = request.headers.get("Authorization")
            if auth_header is None or not auth_header.startswith("Basic "):
                raise CredentialsException(detail="Credentials Necessary", status_code=status.HTTP_401_UNAUTHORIZED)

            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("ascii")
            username, password = decoded_credentials.split(":")
            is_user_valid(credentials=HTTPBasicCredentials(username=username, password=password))
        response = await call_next(request)
        return response
    except (HTTPException, CredentialsException) as e:
        return JSONResponse(content=f"{e.detail}", status_code=e.status_code)


def is_user_valid(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> None:
    correct_username = os.getenv("USERNAME", "")
    correct_password = os.getenv("PASSWORD", "")
    encoded_credentials = base64.b64encode(f"{credentials.username}:{credentials.password}".encode("ascii")).decode("ascii")
    if encoded_credentials != base64.b64encode(f"{correct_username}:{correct_password}".encode("ascii")).decode("ascii"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
