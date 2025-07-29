"""Data models for XDBC API responses"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class XDBResponse:
    """Response model for XDBC API calls"""
    status: str
    message: str = ""
    data: Optional[Any] = None
    error: bool = False