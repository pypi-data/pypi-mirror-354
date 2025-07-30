from enum import Enum
from typing import Dict, Optional, Tuple, Union

from pydantic import AnyHttpUrl, BaseModel, validator, field_validator, Field


class HttpMethod(str, Enum):
    """
    Enumeration for HTTP methods.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class RequestInfo(BaseModel):
    """
    Information about an HTTP request.

    Attributes:
        url (AnyHttpUrl): The URL for the request.
        payload (Optional[Union[Dict, list]]): The payload for the request, if any.
        verify (bool): Whether to verify the server's TLS certificate.
        method (HttpMethod): The HTTP method for the request. Defaults to POST.
        timeout (Optional[Union[float, Tuple[float, float], Tuple[float, None]]]): The timeout for the request.
        headers (Optional[Dict[str, str]]): Headers to be sent with the request.
        params (Optional[Dict[str, Union[str, int, float]]]): URL parameters for the request.
    """
    url: AnyHttpUrl
    payload: Optional[Union[Dict, list]]
    verify: bool = True
    method: HttpMethod = HttpMethod.POST
    timeout: Optional[Union[float, Tuple[float, float], Tuple[float, None]]] = (
        20,
        60 * 30,
    )
    headers: Optional[Dict[str, str]] = Field(default_factory=lambda: {"Content-Type": "application/json"})
    params: Optional[Dict[str, Union[str, int, float]]] = None

    @field_validator("method", mode="before")
    @classmethod
    def uppercase_method(cls, v) -> str:
        """
        Ensures that the HTTP method is in uppercase.

        Args:
            v: The HTTP method.

        Returns:
            The HTTP method in uppercase.
        """
        return v.upper() if isinstance(v, str) else v
