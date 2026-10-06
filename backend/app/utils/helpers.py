"""
Helper utilities for AyurScan backend.
"""

import re
from typing import str

def normalize_plant_name(name: str) -> str:
    """Normalizes whitespace and capitalization for botanical lookups."""
    if not name:
        return ""
    cleaned = re.sub(r"\s+", " ", name.strip())
    return cleaned

def format_percentage(score: float) -> str:
    """Formats float confidence (0.0 - 1.0) into user-friendly percent string."""
    return f"{int(round(score * 100))}%"
