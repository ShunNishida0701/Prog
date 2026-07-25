"""好みプロファイル計算のテスト。"""

import pytest

from my_color_recipe_ai.image_features import ImageFeatures
from my_color_recipe_ai.preference import calculate_preference_profile


def make_features(
    brightness: float,
    contrast: float,
    saturation: float,
) -> ImageFeatures:
    """テスト用の特徴量を作成する。"""
    return {
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
    }


def test_calculate_average_profile() -> None:
    feature_list = [
        make_features(0.2, 0.1, 0.4),
        make_features(0.5, 0.3, 0.5),
        make_features(0.8, 0.5, 0.6),
    ]

    profile = calculate_preference_profile(feature_list)

    assert profile["brightness"] == pytest.approx(0.5)
    assert profile["contrast"] == pytest.approx(0.3)
    assert profile["saturation"] == pytest.approx(0.5)
    assert profile["photo_count"] == 3


def test_single_photo_profile() -> None:
    feature_list = [make_features(0.4, 0.2, 0.7)]

    profile = calculate_preference_profile(feature_list)

    assert profile["brightness"] == pytest.approx(0.4)
    assert profile["contrast"] == pytest.approx(0.2)
    assert profile["saturation"] == pytest.approx(0.7)
    assert profile["photo_count"] == 1


def test_empty_feature_list() -> None:
    with pytest.raises(ValueError, match="1枚以上"):
        calculate_preference_profile([])


def test_feature_outside_valid_range() -> None:
    feature_list = [make_features(1.2, 0.2, 0.4)]

    with pytest.raises(ValueError, match="0.0～1.0"):
        calculate_preference_profile(feature_list)
