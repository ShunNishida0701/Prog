"""画像特徴量のテスト。"""

import pytest
from PIL import Image

from my_color_recipe_ai.image_features import extract_features


def test_black_image() -> None:
    image = Image.new("RGB", (10, 10), (0, 0, 0))

    features = extract_features(image)

    assert features["brightness"] == pytest.approx(0.0)
    assert features["contrast"] == pytest.approx(0.0)
    assert features["saturation"] == pytest.approx(0.0)


def test_white_image() -> None:
    image = Image.new("RGB", (10, 10), (255, 255, 255))

    features = extract_features(image)

    assert features["brightness"] == pytest.approx(1.0)
    assert features["contrast"] == pytest.approx(0.0)
    assert features["saturation"] == pytest.approx(0.0)


def test_red_image() -> None:
    image = Image.new("RGB", (10, 10), (255, 0, 0))

    features = extract_features(image)

    assert features["brightness"] == pytest.approx(0.2126)
    assert features["contrast"] == pytest.approx(0.0)
    assert features["saturation"] == pytest.approx(1.0)


def test_gray_image() -> None:
    image = Image.new("RGB", (10, 10), (128, 128, 128))

    features = extract_features(image)

    assert features["brightness"] == pytest.approx(128 / 255)
    assert features["contrast"] == pytest.approx(0.0)
    assert features["saturation"] == pytest.approx(0.0)


def test_invalid_input() -> None:
    with pytest.raises(TypeError):
        extract_features("not an image")  # type: ignore[arg-type]
