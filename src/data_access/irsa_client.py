"""Direct HTTP client for the IRSA Simple Image Access (SIA2) service.

This module intentionally avoids PyVO and Astropy so archive metadata searches
can run in environments where compiled astronomy extensions are restricted.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd
import requests

IRSA_SIA2_URL = "https://irsa.ipac.caltech.edu/SIA"
REQUEST_TIMEOUT_SECONDS = 45
MAX_RECORDS = 2000


class IRSAQueryError(RuntimeError):
    """Raised when an IRSA archive query fails."""


def query_sia2(
    *, ra_deg: float, dec_deg: float, radius_deg: float, collection: str
) -> pd.DataFrame:
    """Query IRSA SIA2 and return its CSV metadata response as a DataFrame.

    POS uses the SIA2 CIRCLE syntax: centre RA, centre Dec, and angular radius,
    all in degrees.
    """
    if not 0.0 <= ra_deg <= 360.0:
        raise ValueError("RA must be between 0 and 360 degrees.")
    if not -90.0 <= dec_deg <= 90.0:
        raise ValueError("Dec must be between -90 and 90 degrees.")
    if radius_deg <= 0:
        raise ValueError("Search radius must be greater than zero.")
    if not collection.strip():
        raise ValueError("Collection must not be empty.")

    params = [
        ("COLLECTION", collection),
        ("POS", f"CIRCLE {ra_deg:.8f} {dec_deg:.8f} {radius_deg:.8f}"),
        ("RESPONSEFORMAT", "CSV"),
        ("MAXREC", str(MAX_RECORDS)),
    ]

    try:
        response = requests.get(
            IRSA_SIA2_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise IRSAQueryError(
            f"Could not contact IRSA SIA2 for collection '{collection}': {exc}"
        ) from exc

    body = response.text.strip()
    if not body:
        raise IRSAQueryError(
            f"IRSA returned an empty response for collection '{collection}'."
        )

    try:
        frame = pd.read_csv(StringIO(body))
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as exc:
        preview = body[:500].replace("\n", " ")
        raise IRSAQueryError(
            "IRSA did not return a readable CSV response. "
            f"Response preview: {preview}"
        ) from exc

    return frame
