from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse


dynamics_router = APIRouter(tags=["AppDynamics"])

@dynamics_router.post('/alerts')
async def receive_alerts(request: Request):
    return JSONResponse(
        content="Success Validation",
        status_code=status.HTTP_200_OK
    )
