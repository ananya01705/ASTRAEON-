import numpy as np
import pytest

from src.processing.image_inspection import summarize_image_array


def test_summarize_image_array_returns_basic_statistics():
    result = summarize_image_array(np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert result["pixel_count"] == 4
    assert result["finite_pixel_count"] == 4
    assert result["minimum"] == 1.0
    assert result["maximum"] == 4.0
    assert result["mean"] == 2.5


def test_summarize_image_array_ignores_non_finite_pixels():
    result = summarize_image_array(np.array([[1.0, np.nan], [3.0, np.inf]]))
    assert result["pixel_count"] == 4
    assert result["finite_pixel_count"] == 2
    assert result["mean"] == 2.0


def test_summarize_image_array_rejects_all_non_finite_data():
    with pytest.raises(ValueError):
        summarize_image_array(np.array([[np.nan, np.inf]]))
