"""Basic image-array checks; no temporal analysis is performed here."""

from __future__ import annotations

import numpy as np


def summarize_image_array(data: np.ndarray) -> dict[str, float | int]:
    """Return finite-pixel statistics for a numeric image array."""
    array = np.asarray(data, dtype=float)
    finite = array[np.isfinite(array)]
    if finite.size == 0:
        raise ValueError("Image contains no finite pixel values.")

    return {
        "pixel_count": int(array.size),
        "finite_pixel_count": int(finite.size),
        "minimum": float(np.min(finite)),
        "maximum": float(np.max(finite)),
        "mean": float(np.mean(finite)),
        "median": float(np.median(finite)),
        "standard_deviation": float(np.std(finite)),
    }
