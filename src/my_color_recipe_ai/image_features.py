"""画像から基本的な色特徴量を計算する機能。"""

from typing import TypedDict

import numpy as np
from numpy.typing import NDArray
from PIL import Image


class ImageFeatures(TypedDict):
    """画像から抽出した特徴量。"""

    brightness: float
    contrast: float
    saturation: float


def image_to_array(image: Image.Image) -> NDArray[np.float64]:
    """Pillow画像を0.0～1.0のRGB配列へ変換する。"""
    if not isinstance(image, Image.Image):
        raise TypeError("imageにはPillowのImageオブジェクトを指定してください。")

    rgb_image = image.convert("RGB")
    return np.asarray(rgb_image, dtype=np.float64) / 255.0


def _calculate_luminance(
    image_array: NDArray[np.float64],
) -> NDArray[np.float64]:
    """RGB配列から画素ごとの輝度を計算する。"""
    red = image_array[..., 0]
    green = image_array[..., 1]
    blue = image_array[..., 2]

    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def calculate_brightness(image_array: NDArray[np.float64]) -> float:
    """画像全体の平均的な明るさを計算する。"""
    luminance = _calculate_luminance(image_array)
    return float(np.mean(luminance))


def calculate_contrast(image_array: NDArray[np.float64]) -> float:
    """輝度の標準偏差からコントラストを計算する。"""
    luminance = _calculate_luminance(image_array)
    return float(np.std(luminance))


def calculate_saturation(image_array: NDArray[np.float64]) -> float:
    """RGBの最大値と最小値から平均彩度を計算する。"""
    maximum = np.max(image_array, axis=2)
    minimum = np.min(image_array, axis=2)

    saturation = np.divide(
        maximum - minimum,
        maximum,
        out=np.zeros_like(maximum),
        where=maximum != 0,
    )
    return float(np.mean(saturation))


def extract_features(image: Image.Image) -> ImageFeatures:
    """画像から明るさ・コントラスト・彩度をまとめて抽出する。"""
    image_array = image_to_array(image)

    return {
        "brightness": calculate_brightness(image_array),
        "contrast": calculate_contrast(image_array),
        "saturation": calculate_saturation(image_array),
    }
