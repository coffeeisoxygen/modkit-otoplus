from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.mlog.cst_logging import logger, patch_uvicorn_loggers, setup_logging

# Ensure logging is set up before using the middleware
setup_logging()
patch_uvicorn_loggers()


class LogIpMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Middleware to log the IP address of incoming requests.

        This middleware extracts the client's IP address from the request and binds it to the logger context.

        Args:
            request (Request): The incoming request object.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The response object returned by the next middleware or endpoint.
        """
        client_ip = request.client.host if request.client else "unknown"
        logger_ = logger.bind(ip=client_ip)
        # Pasang logger yang sudah bind ke context request
        request.state.logger = logger_
        response = await call_next(request)

        return response
