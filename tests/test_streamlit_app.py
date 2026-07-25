"""Streamlitアプリ全体のスモークテスト。"""

from io import BytesIO

from PIL import Image
from streamlit.testing.v1 import AppTest


def create_png_bytes(color: tuple[int, int, int]) -> bytes:
    """テスト用PNG画像をメモリ上に作成する。"""
    image = Image.new("RGB", (20, 20), color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_app_starts_without_exception() -> None:
    app = AppTest.from_file("streamlit_app.py").run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "My Color Recipe AI"
    assert len(app.file_uploader) == 1


def test_complete_image_workflow() -> None:
    app = AppTest.from_file("streamlit_app.py").run(timeout=30)

    preference_images = [
        ("dark.png", create_png_bytes((50, 50, 50)), "image/png"),
        ("warm.png", create_png_bytes((200, 120, 80)), "image/png"),
    ]

    app.file_uploader[0].set_value(preference_images).run(timeout=30)

    assert not app.exception
    assert len(app.file_uploader) == 2

    target_uploader = app.file_uploader(key="target_image")
    target_uploader.upload(
        "target.png",
        create_png_bytes((100, 150, 200)),
        "image/png",
    ).run(timeout=30)

    assert not app.exception
    assert len(app.dataframe) >= 3
