# necta_fetcher/exceptions.py

class NectaError(Exception):
    """Base exception for the necta_fetcher package."""
    pass

class NectaLoginError(NectaError):
    """Raised when login to the NECTA portal fails."""
    pass

class NectaTokenError(NectaError):
    """Raised when CSRF token extraction or handling fails."""
    pass

class NectaRequestError(NectaError):
    """Raised for network or HTTP errors during requests to NECTA portal."""
    pass

class NectaResultError(NectaError):
    """Raised when fetching or parsing results fails, or API returns an error."""
    pass

class NectaStudentNotFoundError(NectaResultError):
    """
    Raised when a specific student is not found, either because the API
    indicates so, or the expected data structure for a student is missing,
    or an 'N/A' placeholder is returned for the specific student query.
    """
    pass