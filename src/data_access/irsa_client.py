"""Minimal client for the IRSA Simple Image Access (SIA2) service."""

from __future__ import annotations

import pyvo

IRSA_SIA2_URL = "https://irsa.ipac.caltech.edu/SIA"


class IRSAQueryError(RuntimeError):
    """Raised when an IRSA archive query fails."""


def query_sia2(*, ra_deg: float, dec_deg: float, radius_deg: float, collection: str):
    """Return a PyVO SIA2 result table for an ICRS sky position.

    The search size is a square width in degrees. It is deliberately kept
    small for the first feasibility tests.
    """
    if not 0.0 <= ra_deg <= 360.0:
        raise ValueError("RA must be between 0 and 360 degrees.")
    if not -90.0 <= dec_deg <= 90.0:
        raise ValueError("Dec must be between -90 and 90 degrees.")
    if radius_deg <= 0:
        raise ValueError("Search radius must be greater than zero.")
    if not collection.strip():
        raise ValueError("Collection must not be empty.")

    try:
        service = pyvo.dal.SIA2Service(IRSA_SIA2_URL)
        return service.search(
            pos=(ra_deg, dec_deg),
            size=radius_deg * 2.0,
            collection=collection,
        )
    except Exception as exc:
        raise IRSAQueryError(
            f"IRSA SIA2 query failed for collection '{collection}': {exc}"
        ) from exc
