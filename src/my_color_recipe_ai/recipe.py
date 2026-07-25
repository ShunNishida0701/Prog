"""好みプロファイルから写真の加工レシピを提案する機能。"""

from collections.abc import Mapping
from typing import TypedDict

from my_color_recipe_ai.image_features import ImageFeatures
from my_color_recipe_ai.preference import PreferenceProfile


class PhotoRecipe(TypedDict):
    """写真に適用する特徴量ごとの変更量。"""

    brightness_change: float
    contrast_change: float
    saturation_change: float


FEATURE_NAMES = ("brightness", "contrast", "saturation")


def _validate_features(
    features: Mapping[str, object],
    input_name: str,
) -> None:
    """特徴量が存在し、0.0～1.0の範囲にあることを確認する。"""
    for feature_name in FEATURE_NAMES:
        value = features.get(feature_name)

        if not isinstance(value, (int, float)):
            raise TypeError(f"{input_name}の{feature_name}が数値ではありません。")

        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(
                f"{input_name}の{feature_name}は0.0～1.0の範囲で指定してください。"
            )


def suggest_recipe(
    preference_profile: PreferenceProfile,
    target_features: ImageFeatures,
) -> PhotoRecipe:
    """好みと加工対象写真の差から加工レシピを提案する。"""
    _validate_features(preference_profile, "好みプロファイル")
    _validate_features(target_features, "加工対象写真")

    return {
        "brightness_change": (
            preference_profile["brightness"] - target_features["brightness"]
        ),
        "contrast_change": (
            preference_profile["contrast"] - target_features["contrast"]
        ),
        "saturation_change": (
            preference_profile["saturation"] - target_features["saturation"]
        ),
    }
