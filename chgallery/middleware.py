"""Middleware classes."""

from typing import Any, Dict, Union


class PrefixMiddleware:
    """Provides common root url prefix when application is mounted outside server root."""

    def __init__(self, app: Any, prefix: str = "") -> None:
        self.app = app
        self.prefix = prefix

    def __call__(
        self, environ: Dict[str, Any], start_response: Any
    ) -> Union[Any, list[bytes]]:
        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)

        start_response("404", [("Content-Type", "text/plain")])
        return ["This url does not belong to the app.".encode()]
