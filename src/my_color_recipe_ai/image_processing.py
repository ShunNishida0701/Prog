"""加工レシピに従って画像を調整する機能。"""

from PIL import Image, ImageEnhance

from my_color_recipe_ai.recipe import PhotoRecipe

CHANGE_NAMES = (
    "brightness_change",
    "contrast_change",
    "saturation_change",
)


def _validate_recipe(recipe: PhotoRecipe) -> None:
    """レシピの変更量が-1.0～1.0であることを確認する。"""
    for change_name in CHANGE_NAMES:
        value = recipe.get(change_name)

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{change_name}が数値ではありません。")

        if not -1.0 <= float(value) <= 1.0:
            raise ValueError(f"{change_name}は-1.0～1.0の範囲で指定してください。")


def _change_to_factor(change: float) -> float:
    """特徴量の変更量をPillowの処理係数へ変換する。"""
    return 1.0 + change


def apply_recipe(
    image: Image.Image,
    recipe: PhotoRecipe,
) -> Image.Image:
    """明るさ・コントラスト・彩度を順番に調整する。"""
    if not isinstance(image, Image.Image):
        raise TypeError("imageにはPillowのImageオブジェクトを指定してください。")

    _validate_recipe(recipe)

    processed_image = image.convert("RGB").copy()

    brightness_factor = _change_to_factor(recipe["brightness_change"])
    processed_image = ImageEnhance.Brightness(processed_image).enhance(
        brightness_factor
    )

    contrast_factor = _change_to_factor(recipe["contrast_change"])
    processed_image = ImageEnhance.Contrast(processed_image).enhance(contrast_factor)

    saturation_factor = _change_to_factor(recipe["saturation_change"])
    processed_image = ImageEnhance.Color(processed_image).enhance(saturation_factor)

    return processed_image
