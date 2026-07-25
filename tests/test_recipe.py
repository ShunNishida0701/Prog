"""加工レシピ提案のテスト。"""

import pytest

from my_color_recipe_ai.image_features import ImageFeatures
from my_color_recipe_ai.preference import PreferenceProfile
from my_color_recipe_ai.recipe import suggest_recipe


def make_profile(
    brightness: float,
    contrast: float,
    saturation: float,
) -> PreferenceProfile:
    """テスト用の好みプロファイルを作成する。"""
    return {
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
        "photo_count": 3,
    }


def make_features(
    brightness: float,
    contrast: float,
    saturation: float,
) -> ImageFeatures:
    """テスト用の画像特徴量を作成する。"""
    return {
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
    }


def test_suggest_recipe() -> None:
    profile = make_profile(0.7, 0.3, 0.8)
    target = make_features(0.4, 0.5, 0.2)

    recipe = suggest_recipe(profile, target)

    assert recipe["brightness_change"] == pytest.approx(0.3)
    assert recipe["contrast_change"] == pytest.approx(-0.2)
    assert recipe["saturation_change"] == pytest.approx(0.6)


def test_matching_photo_produces_zero_changes() -> None:
    profile = make_profile(0.5, 0.4, 0.3)
    target = make_features(0.5, 0.4, 0.3)

    recipe = suggest_recipe(profile, target)

    assert recipe["brightness_change"] == pytest.approx(0.0)
    assert recipe["contrast_change"] == pytest.approx(0.0)
    assert recipe["saturation_change"] == pytest.approx(0.0)


def test_recipe_can_decrease_features() -> None:
    profile = make_profile(0.2, 0.3, 0.4)
    target = make_features(0.8, 0.7, 0.6)

    recipe = suggest_recipe(profile, target)

    assert recipe["brightness_change"] < 0.0
    assert recipe["contrast_change"] < 0.0
    assert recipe["saturation_change"] < 0.0


def test_invalid_target_feature() -> None:
    profile = make_profile(0.5, 0.5, 0.5)
    target = make_features(1.2, 0.5, 0.5)

    with pytest.raises(ValueError, match="0.0～1.0"):
        suggest_recipe(profile, target)
