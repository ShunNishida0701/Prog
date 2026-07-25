"""基本レシピから複数の加工パターンを生成する機能。"""

from dataclasses import dataclass

from my_color_recipe_ai.recipe import PhotoRecipe


@dataclass(frozen=True)
class StyleDefinition:
    """加工スタイルの定義。"""

    style_id: str
    name: str
    description: str
    brightness_offset: float
    contrast_offset: float
    saturation_offset: float


@dataclass(frozen=True)
class RecipeVariation:
    """画面に表示する加工候補。"""

    style_id: str
    name: str
    description: str
    recipe: PhotoRecipe


STYLE_DEFINITIONS = (
    StyleDefinition(
        style_id="faithful",
        name="好みに忠実",
        description="好み写真の平均に近づける基本候補です。",
        brightness_offset=0.0,
        contrast_offset=0.0,
        saturation_offset=0.0,
    ),
    StyleDefinition(
        style_id="clear",
        name="鮮明・クリア",
        description="明るさとコントラストを少し高めます。",
        brightness_offset=0.05,
        contrast_offset=0.15,
        saturation_offset=0.05,
    ),
    StyleDefinition(
        style_id="nostalgic",
        name="ノスタルジック",
        description="コントラストと彩度を抑えた柔らかい候補です。",
        brightness_offset=-0.05,
        contrast_offset=-0.05,
        saturation_offset=-0.15,
    ),
    StyleDefinition(
        style_id="cinematic",
        name="ダーク・シネマ",
        description="明るさを抑え、コントラストを高めます。",
        brightness_offset=-0.20,
        contrast_offset=0.20,
        saturation_offset=-0.10,
    ),
    StyleDefinition(
        style_id="airy",
        name="明るい・エアリー",
        description="明るく、コントラストと彩度を控えめにします。",
        brightness_offset=0.20,
        contrast_offset=-0.10,
        saturation_offset=-0.10,
    ),
    StyleDefinition(
        style_id="pop",
        name="鮮やか・ポップ",
        description="明るさ、コントラスト、彩度を高めます。",
        brightness_offset=0.10,
        contrast_offset=0.15,
        saturation_offset=0.25,
    ),
)


def _clamp_change(value: float) -> float:
    """変更量を-1.0～1.0へ制限する。"""
    return max(-1.0, min(1.0, value))


def generate_recipe_variations(
    base_recipe: PhotoRecipe,
) -> list[RecipeVariation]:
    """基本レシピから6種類の加工候補を生成する。"""
    variations: list[RecipeVariation] = []

    for style in STYLE_DEFINITIONS:
        recipe: PhotoRecipe = {
            "brightness_change": _clamp_change(
                base_recipe["brightness_change"] + style.brightness_offset
            ),
            "contrast_change": _clamp_change(
                base_recipe["contrast_change"] + style.contrast_offset
            ),
            "saturation_change": _clamp_change(
                base_recipe["saturation_change"] + style.saturation_offset
            ),
        }

        variations.append(
            RecipeVariation(
                style_id=style.style_id,
                name=style.name,
                description=style.description,
                recipe=recipe,
            )
        )

    return variations
