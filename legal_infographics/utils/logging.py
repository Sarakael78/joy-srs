"""
Logging configuration for the Legal Strategy Infographics Platform.
"""

import logging
import sys
from typing import Optional

from ..config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Setup logging configuration."""
    if log_level is None:
        log_level = settings.monitoring.log_level

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log"),
        ],
    )

    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
