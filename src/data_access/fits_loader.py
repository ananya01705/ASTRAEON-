"""FITS inspection placeholder for environments without an approved FITS reader.

The initial archive-search milestone deliberately does not import Astropy.
FITS inspection will be re-enabled once a compatible, permitted astronomy
environment is available.
"""

from __future__ import annotations

from typing import Any


class FITSInspectionUnavailable(RuntimeError):
    """Raised when FITS inspection is not available in the current build."""


def inspect_fits_url(url: str, *, timeout: int = 60) -> dict[str, Any]:
    """Placeholder: FITS inspection is not part of the metadata-only milestone."""
    del url, timeout
    raise FITSInspectionUnavailable(
        "FITS inspection is temporarily disabled. The current build supports "
        "IRSA archive metadata searches only; no FITS files are downloaded "
        "or interpreted."
    )
