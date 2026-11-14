"""Search SPHEREx collections and normalize observation metadata."""

from __future__ import annotations

import pandas as pd

from src.data_access.irsa_client import IRSAQueryError, query_sia2

SUPPORTED_COLLECTIONS = {"spherex_dr1", "spherex_qr3"}


def search_spherex_observations(
    *, ra_deg: float, dec_deg: float, radius_arcmin: float, collections: list[str]
) -> pd.DataFrame:
    """Query selected collections and combine the returned metadata rows."""
    if radius_arcmin <= 0:
        raise ValueError("Search radius must be greater than zero.")
    if not collections:
        raise ValueError("Select at least one collection.")

    unknown = sorted(set(collections) - SUPPORTED_COLLECTIONS)
    if unknown:
        raise ValueError(f"Unsupported collection(s): {', '.join(unknown)}")

    radius_deg = radius_arcmin / 60.0
    frames: list[pd.DataFrame] = []
    errors: list[str] = []

    for collection in collections:
        try:
            frame = query_sia2(
                ra_deg=ra_deg,
                dec_deg=dec_deg,
                radius_deg=radius_deg,
                collection=collection,
            )
            frame["queried_collection"] = collection
            frames.append(frame)
        except IRSAQueryError as exc:
            errors.append(str(exc))

    if not frames:
        detail = " | ".join(errors) if errors else "No result tables were returned."
        raise IRSAQueryError(detail)

    combined = pd.concat(frames, ignore_index=True, sort=False)
    if not combined.empty:
        combined = combined.drop_duplicates().reset_index(drop=True)
    return combined
