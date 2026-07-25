"""加工パターン生成のテスト。"""

import pytest

from my_color_recipe_ai.recipe import PhotoRecipe
from my_color_recipe_ai.variations import generate_recipe_variations


def make_base_recipe(
    brightness: float = 0.0,
    contrast: float = 0.0,
    saturation: float = 0.0,
) -> PhotoRecipe:
    """テスト用の基本レシピを作成する。"""
    return {
        "brightness_change": brightness,
        "contrast_change": contrast,
        "saturation_change": saturation,
    }


def test_generate_six_variations() -> None:
    variations = generate_recipe_variations(make_base_recipe())

    assert len(variations) == 6
    assert len({variation.style_id for variation in variations}) == 6


def test_expected_style_names() -> None:
    variations = generate_recipe_variations(make_base_recipe())

    names = [variation.name for variation in variations]

    assert names == [
        "好みに忠実",
        "鮮明・クリア",
        "ノスタルジック",
        "ダーク・シネマ",
        "明るい・エアリー",
        "鮮やか・ポップ",
    ]


def test_faithful_style_uses_base_recipe() -> None:
    base_recipe = make_base_recipe(0.2, -0.1, 0.3)

    faithful = generate_recipe_variations(base_recipe)[0]

    assert faithful.recipe == base_recipe


def test_pop_style_adds_expected_offsets() -> None:
    base_recipe = make_base_recipe(0.1, 0.1, 0.1)

    pop = generate_recipe_variations(base_recipe)[5]

    assert pop.recipe["brightness_change"] == pytest.approx(0.2)
    assert pop.recipe["contrast_change"] == pytest.approx(0.25)
    assert pop.recipe["saturation_change"] == pytest.approx(0.35)


def test_changes_are_clamped_to_valid_range() -> None:
    base_recipe = make_base_recipe(0.95, -0.95, 0.95)

    variations = generate_recipe_variations(base_recipe)

    for variation in variations:
        for value in variation.recipe.values():
            assert -1.0 <= value <= 1.0
