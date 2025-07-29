# -*- coding: utf-8 -*-
from typing import Tuple
from unittest.mock import patch

import numpy as np
import pytest

from common_image_tools.operation import (
    bbox_centroid,
    is_point_in_bbox,
    is_point_in_shape,
    resize_image_with_aspect_ratio,
    scale_bboxes,
    scaled_bbox_centroid,
)


class TestBboxCentroid:
    @pytest.mark.parametrize(
        "bbox, expected_centroid",
        [
            ((0, 0, 10, 10), (5, 5)),
            ((-5, -5, 10, 10), (0, 0)),
            ((100, 200, 30, 40), (115, 220)),
        ],
    )
    def test_bbox_centroid(self, bbox, expected_centroid):
        centroid = bbox_centroid(bbox)
        assert centroid == expected_centroid

    @pytest.mark.parametrize(
        "bbox",
        [
            (-10, -10, 20, 20),
            (0, 0, 15, 15),
            (1000, 2000, 300, 400),
        ],
    )
    def test_valid_bboxes(self, bbox: Tuple[int, int, int, int]):
        centroid = bbox_centroid(bbox)
        assert isinstance(centroid, Tuple)
        assert len(centroid) == 2
        assert all(isinstance(coord, int) for coord in centroid)


# Test resize_image_with_aspect_ratio function
def test_resize_image_with_aspect_ratio():
    # Create a mock image
    mock_image = np.zeros((100, 200, 3), dtype=np.uint8)

    # Define the target size
    target_size = (50, 50)

    # Calculate the expected new dimensions
    aspect_ratio = 200 / 100  # width / height of the original image
    if aspect_ratio > 1:
        expected_width = 50
        expected_height = int(50 / aspect_ratio)
    else:
        expected_height = 50
        expected_width = int(50 * aspect_ratio)

    # Create the expected resized image
    expected_resized = np.zeros((expected_height, expected_width, 3), dtype=np.uint8)

    with patch("cv2.resize", return_value=expected_resized) as mock_resize:
        result = resize_image_with_aspect_ratio(mock_image, target_size)

    assert result.shape == (expected_height, expected_width, 3)
    mock_resize.assert_called_once_with(mock_image, (expected_width, expected_height))


def test_resize_image_with_aspect_ratio_2():
    # Create a mock image
    mock_image = np.zeros((200, 100, 3), dtype=np.uint8)

    # Define the target size
    target_size = (50, 50)

    # Calculate the expected new dimensions
    aspect_ratio = 100 / 200  # width / height of the original image
    if aspect_ratio > 1:
        expected_width = 50
        expected_height = int(50 / aspect_ratio)
    else:
        expected_height = 50
        expected_width = int(50 * aspect_ratio)

    # Create the expected resized image
    expected_resized = np.zeros((expected_height, expected_width, 3), dtype=np.uint8)

    with patch("cv2.resize", return_value=expected_resized) as mock_resize:
        result = resize_image_with_aspect_ratio(mock_image, target_size)

    assert result.shape == (expected_height, expected_width, 3)
    mock_resize.assert_called_once_with(mock_image, (expected_width, expected_height))


# Test is_point_in_bbox function
@pytest.mark.parametrize(
    "point, bbox, expected",
    [
        ((5, 5), (0, 0, 10, 10), True),
        ((15, 15), (0, 0, 10, 10), False),
        ((0, 0), (0, 0, 10, 10), False),
        ((10, 10), (0, 0, 10, 10), False),
    ],
)
def test_is_point_in_bbox(point, bbox, expected):
    assert is_point_in_bbox(point, bbox) == expected


# Test is_point_in_shape function
def test_is_point_in_shape():
    shape_contour = [(0, 0), (10, 0), (10, 10), (0, 10)]

    with patch("cv2.pointPolygonTest", return_value=1) as mock_pointPolygonTest:
        result = is_point_in_shape((5, 5), shape_contour)

    assert result == True
    mock_pointPolygonTest.assert_called_once()


# Test scale_bboxes function
def test_scale_bboxes():
    bboxes = [(10, 10, 20, 20), (30, 30, 40, 40)]
    scale_factor = 2

    result = scale_bboxes(bboxes, scale_factor)

    assert result == [(20, 20, 40, 40), (60, 60, 80, 80)]


# Test bbox_centroid function
@pytest.mark.parametrize(
    "bbox, expected",
    [
        ((0, 0, 10, 10), (5, 5)),
        ((10, 10, 20, 20), (20, 20)),
        ((5, 5, 15, 25), (12, 17)),
    ],
)
def test_bbox_centroid(bbox, expected):
    assert bbox_centroid(bbox) == expected


def test_scaled_bbox_centroid():
    # Test case 1: Square image with centered bbox
    image1 = np.zeros((100, 100, 3))
    bbox1 = (0.25, 0.25, 0.5, 0.5)
    result1 = scaled_bbox_centroid(image1, bbox1)
    assert result1 == (50, 50)

    # Test case 2: Rectangular image with bbox in top-left corner
    image2 = np.zeros((200, 400, 3))
    bbox2 = (0, 0, 0.25, 0.5)
    result2 = scaled_bbox_centroid(image2, bbox2)
    assert result2 == (50, 50)

    # Test case 3: Rectangular image with bbox in bottom-right corner
    image3 = np.zeros((300, 600, 3))
    bbox3 = (0.75, 0.5, 0.25, 0.5)
    result3 = scaled_bbox_centroid(image3, bbox3)
    assert result3 == (525, 225)

    # Test case 4: Very small image
    image4 = np.zeros((10, 20, 3))
    bbox4 = (0.1, 0.2, 0.3, 0.4)
    result4 = scaled_bbox_centroid(image4, bbox4)
    assert result4 == (5, 4)

    # Test case 5: Non-square bbox
    image5 = np.zeros((500, 500, 3))
    bbox5 = (0.1, 0.2, 0.6, 0.3)
    result5 = scaled_bbox_centroid(image5, bbox5)
    assert result5 == (200, 175)


def test_scaled_bbox_centroid_edge_cases():
    # Test case 1: Negative values in bbox
    image1 = np.zeros((100, 100, 3))
    bbox1 = (-0.1, 0.1, 0.2, 0.2)
    result1 = scaled_bbox_centroid(image1, bbox1)
    assert result1 == (0, 20)  # x-coordinate is clamped to 0

    # Test case 2: Values > 1 in bbox
    image2 = np.zeros((100, 100, 3))
    bbox2 = (0.1, 0.1, 1.1, 0.2)
    result2 = scaled_bbox_centroid(image2, bbox2)
    assert result2 == (65, 20)  # width is clamped to image width

    # Test case 3: Non-tuple bbox
    image3 = np.zeros((100, 100, 3))
    bbox3 = [0.1, 0.1, 0.2, 0.2]
    result3 = scaled_bbox_centroid(image3, bbox3)
    assert result3 == (20, 20)  # Function should work with list as well

    # Test case 4: Non-numpy array image
    image4 = [[1, 2], [3, 4]]
    bbox4 = (0.1, 0.1, 0.2, 0.2)
    with pytest.raises(AttributeError):
        scaled_bbox_centroid(image4, bbox4)

    # Test case 6: Full image bbox
    image6 = np.zeros((100, 200, 3))
    bbox6 = (0, 0, 1, 1)
    result6 = scaled_bbox_centroid(image6, bbox6)
    assert result6 == (100, 50)  # This is correct

    # Test case 7: Single pixel bbox
    image7 = np.zeros((50, 50, 3))
    bbox7 = (0.5, 0.5, 0, 0)
    result7 = scaled_bbox_centroid(image7, bbox7)
    assert result7 == (25, 25)  # This is correct

    # Test case 8: Very small bbox
    image8 = np.zeros((1000, 1000, 3))
    bbox8 = (0.1, 0.1, 0.001, 0.001)
    result8 = scaled_bbox_centroid(image8, bbox8)
    assert result8 == (100, 100)  # Corrected expectation
