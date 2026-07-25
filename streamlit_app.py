"""My Color Recipe AIのStreamlit画面。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError

from my_color_recipe_ai.image_features import ImageFeatures, extract_features
from my_color_recipe_ai.image_processing import apply_recipe
from my_color_recipe_ai.preference import calculate_preference_profile
from my_color_recipe_ai.recipe import suggest_recipe
from my_color_recipe_ai.storage import (
    image_to_bytes,
    recipe_to_csv,
    recipe_to_json,
)

st.set_page_config(
    page_title="My Color Recipe AI",
    page_icon="🎨",
    layout="wide",
)

st.title("My Color Recipe AI")
st.write("好きな写真を分析し、明るさ・コントラスト・彩度の傾向を確認します。")

uploaded_files = st.file_uploader(
    "分析するJPEG・PNG画像を選択してください",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info("分析する画像を1枚以上アップロードしてください。")
    st.stop()

analysis_results: list[dict[str, str | float]] = []
preference_features: list[ImageFeatures] = []

for uploaded_file in uploaded_files:
    try:
        with Image.open(uploaded_file) as source_image:
            image = source_image.convert("RGB")

        features = extract_features(image)
        preference_features.append(features)

        analysis_results.append(
            {
                "filename": uploaded_file.name,
                "brightness": features["brightness"],
                "contrast": features["contrast"],
                "saturation": features["saturation"],
            }
        )

        with st.expander(uploaded_file.name, expanded=True):
            image_column, feature_column = st.columns([2, 1])

            with image_column:
                st.image(image, caption=uploaded_file.name)

            with feature_column:
                st.metric("明るさ", f"{features['brightness']:.3f}")
                st.metric("コントラスト", f"{features['contrast']:.3f}")
                st.metric("彩度", f"{features['saturation']:.3f}")

    except (UnidentifiedImageError, OSError, ValueError) as error:
        st.error(f"{uploaded_file.name}を画像として読み込めませんでした。詳細: {error}")

if not analysis_results:
    st.warning("分析できる画像がありませんでした。")
    st.stop()

preference_profile = calculate_preference_profile(preference_features)

st.subheader("好みの平均プロファイル")
st.write("アップロードした写真の特徴量を平均し、現在の好みの傾向として表示しています。")

profile_columns = st.columns(4)

with profile_columns[0]:
    st.metric("写真枚数", preference_profile["photo_count"])

with profile_columns[1]:
    st.metric("平均明るさ", f"{preference_profile['brightness']:.3f}")

with profile_columns[2]:
    st.metric("平均コントラスト", f"{preference_profile['contrast']:.3f}")

with profile_columns[3]:
    st.metric("平均彩度", f"{preference_profile['saturation']:.3f}")

st.divider()
st.subheader("加工対象写真とレシピ提案")

target_file = st.file_uploader(
    "加工したいJPEG・PNG画像を1枚選択してください",
    type=["jpg", "jpeg", "png"],
    key="target_image",
)

if target_file is None:
    st.info("加工対象写真を選択すると、好みとの差を計算します。")
else:
    try:
        with Image.open(target_file) as source_target_image:
            target_image = source_target_image.convert("RGB")

        target_features = extract_features(target_image)

        suggested_recipe = suggest_recipe(
            preference_profile,
            target_features,
        )

        processed_image = apply_recipe(
            target_image,
            suggested_recipe,
        )
        processed_features = extract_features(processed_image)

        target_image_column, comparison_column = st.columns([2, 3])

        with target_image_column:
            st.image(target_image, caption=target_file.name)

        with comparison_column:
            comparison_dataframe = pd.DataFrame(
                [
                    {
                        "種類": "好みの平均",
                        "明るさ": preference_profile["brightness"],
                        "コントラスト": preference_profile["contrast"],
                        "彩度": preference_profile["saturation"],
                    },
                    {
                        "種類": "加工対象",
                        "明るさ": target_features["brightness"],
                        "コントラスト": target_features["contrast"],
                        "彩度": target_features["saturation"],
                    },
                ]
            )

            st.dataframe(
                comparison_dataframe,
                hide_index=True,
                width="stretch",
                column_config={
                    "明るさ": st.column_config.NumberColumn(format="%.3f"),
                    "コントラスト": st.column_config.NumberColumn(format="%.3f"),
                    "彩度": st.column_config.NumberColumn(format="%.3f"),
                },
            )

        st.write("#### 提案された変更量")
        st.caption("プラスは増加、マイナスは減少を表します。")

        recipe_columns = st.columns(3)

        with recipe_columns[0]:
            st.metric(
                "明るさ",
                f"{suggested_recipe['brightness_change']:+.3f}",
            )

        with recipe_columns[1]:
            st.metric(
                "コントラスト",
                f"{suggested_recipe['contrast_change']:+.3f}",
            )

        with recipe_columns[2]:
            st.metric(
                "彩度",
                f"{suggested_recipe['saturation_change']:+.3f}",
            )

        # ここへ手順3のコードを入れる
        st.write("#### 加工前後の比較")

        before_column, after_column = st.columns(2)

        with before_column:
            st.write("**加工前**")
            st.image(target_image, caption="Before")

        with after_column:
            st.write("**加工後**")
            st.image(processed_image, caption="After")

        result_comparison = pd.DataFrame(
            [
                {
                    "種類": "好みの平均",
                    "明るさ": preference_profile["brightness"],
                    "コントラスト": preference_profile["contrast"],
                    "彩度": preference_profile["saturation"],
                },
                {
                    "種類": "加工前",
                    "明るさ": target_features["brightness"],
                    "コントラスト": target_features["contrast"],
                    "彩度": target_features["saturation"],
                },
                {
                    "種類": "加工後",
                    "明るさ": processed_features["brightness"],
                    "コントラスト": processed_features["contrast"],
                    "彩度": processed_features["saturation"],
                },
            ]
        )

        st.dataframe(
            result_comparison,
            hide_index=True,
            width="stretch",
            column_config={
                "明るさ": st.column_config.NumberColumn(format="%.3f"),
                "コントラスト": st.column_config.NumberColumn(format="%.3f"),
                "彩度": st.column_config.NumberColumn(format="%.3f"),
            },
        )

        st.write("#### 加工結果のダウンロード")

        output_format = st.radio(
            "画像の保存形式",
            options=["PNG", "JPEG"],
            horizontal=True,
            key="output_format",
        )

        image_data = image_to_bytes(processed_image, output_format)
        recipe_json = recipe_to_json(suggested_recipe)
        recipe_csv = recipe_to_csv(suggested_recipe)

        base_filename = Path(target_file.name).stem

        if output_format == "PNG":
            image_extension = "png"
            image_mime = "image/png"
        else:
            image_extension = "jpg"
            image_mime = "image/jpeg"

        download_columns = st.columns(3)

        with download_columns[0]:
            st.download_button(
                label="加工画像を保存",
                data=image_data,
                file_name=(f"{base_filename}_processed.{image_extension}"),
                mime=image_mime,
                key="download_processed_image",
            )

        with download_columns[1]:
            st.download_button(
                label="JSONレシピを保存",
                data=recipe_json,
                file_name=f"{base_filename}_recipe.json",
                mime="application/json",
                key="download_recipe_json",
            )

        with download_columns[2]:
            st.download_button(
                label="CSVレシピを保存",
                data=recipe_csv,
                file_name=f"{base_filename}_recipe.csv",
                mime="text/csv",
                key="download_recipe_csv",
            )

    except (UnidentifiedImageError, OSError, ValueError) as error:
        st.error(f"{target_file.name}を分析できませんでした。詳細: {error}")

results_dataframe = pd.DataFrame(analysis_results)

st.subheader("分析結果一覧")

display_dataframe = results_dataframe.rename(
    columns={
        "filename": "ファイル名",
        "brightness": "明るさ",
        "contrast": "コントラスト",
        "saturation": "彩度",
    }
)

st.dataframe(
    display_dataframe,
    hide_index=True,
    width="stretch",
    column_config={
        "明るさ": st.column_config.NumberColumn(format="%.3f"),
        "コントラスト": st.column_config.NumberColumn(format="%.3f"),
        "彩度": st.column_config.NumberColumn(format="%.3f"),
    },
)

st.subheader("特徴量の比較")

chart_dataframe = results_dataframe[["brightness", "contrast", "saturation"]].copy()
chart_dataframe.index = [
    f"Photo {number}" for number in range(1, len(chart_dataframe) + 1)
]
chart_dataframe.columns = ["Brightness", "Contrast", "Saturation"]

figure, axis = plt.subplots(figsize=(10, 5))
chart_dataframe.plot(kind="bar", ax=axis)

axis.set_xlabel("Uploaded image")
axis.set_ylabel("Feature value")
axis.set_ylim(0.0, 1.0)
axis.tick_params(axis="x", rotation=0)
axis.grid(axis="y", alpha=0.3)
figure.tight_layout()

st.pyplot(figure)
plt.close(figure)
