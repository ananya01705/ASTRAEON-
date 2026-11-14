"""FITS inspection helper; product downloads are explicit, not automatic."""

from __future__ import annotations

from io import BytesIO
from typing import Any

import requests
from astropy.io import fits


def inspect_fits_url(url: str, *, timeout: int = 60) -> dict[str, Any]:
    """Fetch a FITS URL into memory and return basic HDU metadata."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    with fits.open(BytesIO(response.content), memmap=False) as hdul:
        return {
            "hdu_count": len(hdul),
            "hdus": [
                {
                    "index": index,
                    "name": hdu.name,
                    "data_shape": tuple(hdu.data.shape) if hdu.data is not None else None,
                    "data_type": str(hdu.data.dtype) if hdu.data is not None else None,
                }
                for index, hdu in enumerate(hdul)
            ],
        }
