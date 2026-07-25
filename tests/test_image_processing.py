"""画像加工処理のテスト。"""

import numpy as np
import pytest
from PIL import Image

from my_color_recipe_ai.image_features import extract_features
from my_color_recipe_ai.image_processing import apply_recipe
from my_color_recipe_ai.recipe import PhotoRecipe


def make_recipe(
    brightness: float = 0.0,
    contrast: float = 0.0,
    saturation: float = 0.0,
) -> PhotoRecipe:
    """テスト用の加工レシピを作成する。"""
    return {
        "brightness_change": brightness,
        "contrast_change": contrast,
        "saturation_change": saturation,
    }


def test_zero_recipe_does_not_change_image() -> None:
    image = Image.new("RGB", (2, 1))
    image.putdata([(50, 100, 150), (200, 150, 100)])

    processed = apply_recipe(image, make_recipe())

    assert np.array_equal(np.asarray(processed), np.asarray(image))


def test_positive_brightness_makes_image_brighter() -> None:
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    processed = apply_recipe(image, make_recipe(brightness=0.3))

    before = extract_features(image)
    after = extract_features(processed)
    assert after["brightness"] > before["brightness"]


def test_negative_brightness_makes_image_darker() -> None:
    image = Image.new("RGB", (10, 10), (150, 150, 150))

    processed = apply_recipe(image, make_recipe(brightness=-0.3))

    before = extract_features(image)
    after = extract_features(processed)
    assert after["brightness"] < before["brightness"]


def test_increased_contrast_increases_measured_contrast() -> None:
    image = Image.new("RGB", (2, 1))
    image.putdata([(64, 64, 64), (192, 192, 192)])

    processed = apply_recipe(image, make_recipe(contrast=0.5))

    before = extract_features(image)
    after = extract_features(processed)
    assert after["contrast"] > before["contrast"]


def test_saturation_minus_one_creates_grayscale_image() -> None:
    image = Image.new("RGB", (10, 10), (255, 0, 0))

    processed = apply_recipe(image, make_recipe(saturation=-1.0))

    features = extract_features(processed)
    assert features["saturation"] == pytest.approx(0.0)


def test_invalid_recipe_value() -> None:
    image = Image.new("RGB", (10, 10), (100, 100, 100))
    recipe = make_recipe(brightness=1.2)

    with pytest.raises(ValueError, match="-1.0～1.0"):
        apply_recipe(image, recipe)
