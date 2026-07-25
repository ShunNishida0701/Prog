"""保存用データ変換処理のテスト。"""

import json
from io import BytesIO, StringIO

import pandas as pd
import pytest
from PIL import Image

from my_color_recipe_ai.recipe import PhotoRecipe
from my_color_recipe_ai.storage import (
    image_to_bytes,
    recipe_to_csv,
    recipe_to_json,
)


def make_recipe() -> PhotoRecipe:
    """テスト用の加工レシピを作成する。"""
    return {
        "brightness_change": 0.2,
        "contrast_change": -0.1,
        "saturation_change": 0.3,
    }


def test_recipe_to_json() -> None:
    recipe = make_recipe()

    json_text = recipe_to_json(recipe)
    restored_recipe = json.loads(json_text)

    assert restored_recipe == recipe


def test_recipe_to_csv() -> None:
    recipe = make_recipe()

    csv_text = recipe_to_csv(recipe)
    dataframe = pd.read_csv(StringIO(csv_text))

    assert len(dataframe) == 1
    assert dataframe.loc[0, "brightness_change"] == pytest.approx(0.2)
    assert dataframe.loc[0, "contrast_change"] == pytest.approx(-0.1)
    assert dataframe.loc[0, "saturation_change"] == pytest.approx(0.3)


def test_png_image_to_bytes() -> None:
    image = Image.new("RGB", (20, 10), (100, 150, 200))

    image_data = image_to_bytes(image, "PNG")

    with Image.open(BytesIO(image_data)) as restored_image:
        assert restored_image.format == "PNG"
        assert restored_image.size == (20, 10)


def test_jpeg_image_to_bytes() -> None:
    image = Image.new("RGB", (20, 10), (100, 150, 200))

    image_data = image_to_bytes(image, "JPEG")

    with Image.open(BytesIO(image_data)) as restored_image:
        assert restored_image.format == "JPEG"
        assert restored_image.size == (20, 10)


def test_unsupported_image_format() -> None:
    image = Image.new("RGB", (10, 10), (100, 100, 100))

    with pytest.raises(ValueError, match="JPEG, PNG"):
        image_to_bytes(image, "GIF")


def test_invalid_image_input() -> None:
    with pytest.raises(TypeError, match="Pillow"):
        image_to_bytes("not an image", "PNG")  # type: ignore[arg-type]
