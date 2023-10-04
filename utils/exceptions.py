from typing import Any, Dict, Optional
from starlette.exceptions import HTTPException as StarletteHTTPException


class CredentialsException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
