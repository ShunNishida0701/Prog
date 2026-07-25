"""My Color Recipe AIのStreamlit画面。"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError

from my_color_recipe_ai.image_features import ImageFeatures, extract_features
from my_color_recipe_ai.preference import calculate_preference_profile


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
