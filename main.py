from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn
from middleware.auth import apply_basic_auth
from __init__ import __title__, __version__


app = FastAPI(version=__version__, __title__=__title__)
app.middleware('http')(apply_basic_auth)

@app.get('/')
async def root(request: Request):
    return JSONResponse(
        content='Root Page, no authentication necessary',
        status_code=status.HTTP_200_OK
    )

@app.post('/alerts')
async def receive_alerts(request: Request):
    return JSONResponse(
        content="Success Validation",
        status_code=status.HTTP_200_OK
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)