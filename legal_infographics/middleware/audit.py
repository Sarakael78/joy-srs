"""
Audit middleware for request logging.
"""

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class AuditMiddleware(BaseHTTPMiddleware):
    """Audit middleware for comprehensive request logging."""

    async def dispatch(self, request: Request, call_next):
        """Process request with audit logging."""
        start_time = time.time()

        # Log request
        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        user_agent = request.headers.get("user-agent", "")

        logger.info(
            f"Request: {method} {url} from {client_ip} - User-Agent: {user_agent}"
        )

        # Process request
        response = await call_next(request)

        # Log response
        duration = time.time() - start_time
        status_code = response.status_code

        logger.info(
            f"Response: {method} {url} - Status: {status_code} - Duration: {duration:.3f}s"
        )

        return response
