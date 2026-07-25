"""加工画像とレシピを出力用データへ変換する機能。"""

import json
from io import BytesIO

import pandas as pd
from PIL import Image

from my_color_recipe_ai.recipe import PhotoRecipe

from my_color_recipe_ai.image_features import ImageFeatures, extract_features
from my_color_recipe_ai.image_processing import apply_recipe
from my_color_recipe_ai.preference import calculate_preference_profile
from my_color_recipe_ai.recipe import suggest_recipe

SUPPORTED_IMAGE_FORMATS = ("JPEG", "PNG")


def recipe_to_json(recipe: PhotoRecipe) -> str:
    """加工レシピをJSON文字列へ変換する。"""
    return json.dumps(
        recipe,
        ensure_ascii=False,
        indent=2,
    )


def recipe_to_csv(recipe: PhotoRecipe) -> str:
    """加工レシピを1行のCSV文字列へ変換する。"""
    dataframe = pd.DataFrame([recipe])
    return dataframe.to_csv(index=False)


def image_to_bytes(
    image: Image.Image,
    image_format: str,
) -> bytes:
    """Pillow画像をJPEGまたはPNGのバイト列へ変換する。"""
    if not isinstance(image, Image.Image):
        raise TypeError("imageにはPillowのImageオブジェクトを指定してください。")

    normalized_format = image_format.upper()

    if normalized_format not in SUPPORTED_IMAGE_FORMATS:
        supported = ", ".join(SUPPORTED_IMAGE_FORMATS)
        raise ValueError(f"画像形式は{supported}のいずれかを指定してください。")

    output_image = image.convert("RGB")
    output_buffer = BytesIO()

    output_image.save(
        output_buffer,
        format=normalized_format,
        quality=95,
    )

    return output_buffer.getvalue()
