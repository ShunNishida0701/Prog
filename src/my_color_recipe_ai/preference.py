"""複数の好み写真から好みの傾向を計算する機能。"""

from collections.abc import Sequence
from typing import TypedDict

import pandas as pd

from my_color_recipe_ai.image_features import ImageFeatures


class PreferenceProfile(TypedDict):
    """複数写真から計算した好みの特徴。"""

    brightness: float
    contrast: float
    saturation: float
    photo_count: int


FEATURE_NAMES = ("brightness", "contrast", "saturation")


def calculate_preference_profile(
    feature_list: Sequence[ImageFeatures],
) -> PreferenceProfile:
    """複数画像の特徴量から平均的な好みを計算する。"""
    if not feature_list:
        raise ValueError("好みの写真を1枚以上指定してください。")

    dataframe = pd.DataFrame(feature_list)

    missing_features = [
        feature_name
        for feature_name in FEATURE_NAMES
        if feature_name not in dataframe.columns
    ]
    if missing_features:
        missing_text = ", ".join(missing_features)
        raise ValueError(f"必要な特徴量がありません: {missing_text}")

    feature_dataframe = dataframe[list(FEATURE_NAMES)]

    if feature_dataframe.isnull().any().any():
        raise ValueError("特徴量に欠損値が含まれています。")

    outside_range = (feature_dataframe < 0.0) | (feature_dataframe > 1.0)
    if outside_range.any().any():
        raise ValueError("特徴量は0.0～1.0の範囲で指定してください。")

    averages = feature_dataframe.mean()

    return {
        "brightness": float(averages["brightness"]),
        "contrast": float(averages["contrast"]),
        "saturation": float(averages["saturation"]),
        "photo_count": len(feature_list),
    }
