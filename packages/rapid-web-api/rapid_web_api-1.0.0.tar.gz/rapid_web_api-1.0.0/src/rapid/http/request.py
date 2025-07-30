"""
HTTP request parsing and body handling for Rapid
"""

import json
import urllib.parse
from typing import Any, Dict, Optional, Union

from ..utils.json import loads


class Request:
    """
    HTTP request object with body parsing capabilities.

    Supports JSON, form data, and file uploads.
    """

    def __init__(
        self,
        method: str,
        path: str,
        query_string: bytes = b"",
        headers: Dict[str, str] = None,
        body: bytes = b"",
        path_params: Dict[str, Any] = None,
    ):
        self.method = method
        self.path = path
        self.query_string = query_string
        self.headers = headers or {}
        self.body = body
        self.path_params = path_params or {}

        # Parsed data caches
        self._json = None
        self._form = None
        self._query_params = None
        self._files = None

    @property
    def content_type(self) -> str:
        """Get the content type header"""
        return self.headers.get("content-type", "").lower()

    @property
    def content_length(self) -> int:
        """Get the content length"""
        try:
            return int(self.headers.get("content-length", "0"))
        except ValueError:
            return 0

    @property
    def query_params(self) -> Dict[str, str]:
        """Parse and return query parameters"""
        if self._query_params is None:
            self._query_params = {}

            if self.query_string:
                query_str = self.query_string.decode("utf-8")
                self._query_params = dict(
                    urllib.parse.parse_qsl(query_str, keep_blank_values=True)
                )

        return self._query_params

    async def json(self) -> Any:
        """Parse request body as JSON"""
        if self._json is None:
            if not self.body:
                return None

            if "application/json" not in self.content_type:
                raise ValueError("Request content type is not JSON")

            try:
                # Use optimized JSON parsing
                self._json = loads(self.body)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Invalid JSON in request body: {e}")

        return self._json

    async def form(self) -> Dict[str, str]:
        """Parse request body as form data"""
        if self._form is None:
            if not self.body:
                return {}

            if "application/x-www-form-urlencoded" not in self.content_type:
                raise ValueError("Request content type is not form data")

            try:
                body_str = self.body.decode("utf-8")
                self._form = dict(
                    urllib.parse.parse_qsl(body_str, keep_blank_values=True)
                )
            except UnicodeDecodeError as e:
                raise ValueError(f"Invalid form data encoding: {e}")

        return self._form

    async def files(self) -> Dict[str, "UploadFile"]:
        """Parse multipart form data for file uploads"""
        if self._files is None:
            if not self.body:
                return {}

            if "multipart/form-data" not in self.content_type:
                raise ValueError("Request content type is not multipart form data")

            # Extract boundary from content type
            boundary = None
            for part in self.content_type.split(";"):
                part = part.strip()
                if part.startswith("boundary="):
                    boundary = part[9:].strip('"')
                    break

            if not boundary:
                raise ValueError("Missing boundary in multipart form data")

            self._files = self._parse_multipart(boundary)

        return self._files

    def _parse_multipart(self, boundary: str) -> Dict[str, "UploadFile"]:
        """Parse multipart form data"""
        files = {}
        boundary_bytes = f"--{boundary}".encode()

        # Split by boundary
        parts = self.body.split(boundary_bytes)

        for part in parts[1:-1]:  # Skip first and last empty parts
            if not part.strip():
                continue

            # Find headers/body separator
            if b"\r\n\r\n" in part:
                headers_data, file_data = part.split(b"\r\n\r\n", 1)
            else:
                continue

            # Parse headers
            headers_str = headers_data.decode("utf-8", errors="ignore")
            headers = {}

            for line in headers_str.split("\r\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()

            # Extract field name and filename
            disposition = headers.get("content-disposition", "")
            field_name = None
            filename = None

            for param in disposition.split(";"):
                param = param.strip()
                if param.startswith("name="):
                    field_name = param[5:].strip('"')
                elif param.startswith("filename="):
                    filename = param[9:].strip('"')

            if field_name:
                content_type = headers.get("content-type", "application/octet-stream")

                files[field_name] = UploadFile(
                    filename=filename or field_name,
                    content_type=content_type,
                    data=file_data.rstrip(b"\r\n"),
                )

        return files

    async def body_bytes(self) -> bytes:
        """Get raw request body as bytes"""
        return self.body

    async def body_text(self, encoding: str = "utf-8") -> str:
        """Get request body as text"""
        return self.body.decode(encoding)


class UploadFile:
    """
    Represents an uploaded file in multipart form data.
    """

    def __init__(self, filename: str, content_type: str, data: bytes):
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.size = len(data)

    async def read(self, size: int = -1) -> bytes:
        """Read file data"""
        if size == -1:
            return self.data
        return self.data[:size]

    async def write(self, filepath: str):
        """Write file to disk"""
        with open(filepath, "wb") as f:
            f.write(self.data)

    def __repr__(self):
        return f"UploadFile(filename='{self.filename}', size={self.size})"


def parse_request_body(
    body: bytes, content_type: str, encoding: str = "utf-8"
) -> Union[Dict[str, Any], str, bytes]:
    """
    Parse request body based on content type.

    Returns:
        - Dict for JSON and form data
        - str for text content
        - bytes for binary content
    """
    if not body:
        return {}

    content_type = content_type.lower()

    try:
        if "application/json" in content_type:
            body_str = body.decode(encoding)
            return json.loads(body_str)

        elif "application/x-www-form-urlencoded" in content_type:
            body_str = body.decode(encoding)
            return dict(urllib.parse.parse_qsl(body_str, keep_blank_values=True))

        elif "text/" in content_type:
            return body.decode(encoding)

        else:
            # Return raw bytes for binary content
            return body

    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        # Fallback to raw bytes if parsing fails
        return body
