# necta_fetcher/__init__.py
from .client import NectaClient
from .exceptions import (
    NectaError,
    NectaLoginError,
    NectaTokenError,
    NectaRequestError,
    NectaResultError,
    NectaStudentNotFoundError
)

__version__ = "0.5.0" # Initial version

__all__ = [
    "NectaClient",
    "NectaError",
    "NectaLoginError",
    "NectaTokenError",
    "NectaRequestError",
    "NectaResultError",
    "NectaStudentNotFoundError",
   
]