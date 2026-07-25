# My Color Recipe AI

[![CI](https://github.com/ShunNishida0701/Prog/actions/workflows/test.yml/badge.svg)](https://github.com/ShunNishida0701/Prog/actions/workflows/test.yml)

好みの写真を複数分析し、別の写真に適用する加工レシピを提案するPythonアプリです。

## 目的

写真を加工するとき、毎回スライダーを調整して好みの雰囲気を再現するには時間がかかります。

My Color Recipe AIは、ユーザーが好きな写真から明るさ、コントラスト、彩度の傾向を数値化し、加工対象写真との差に基づいて加工レシピを提案します。

## 主な機能

- JPEG・PNG画像の複数アップロード
- 明るさ、コントラスト、彩度の分析
- Pandasによる好み写真の平均プロファイル計算
- 特徴量比較グラフ
- 加工対象写真と好みプロファイルの比較
- 明るさ、コントラスト、彩度の変更量提案
- Pillowによる画像の自動加工
- Before／After表示
- 加工画像のPNG・JPEG保存
- 加工レシピのJSON・CSV保存
- 好みプロファイルを基準とした6種類の加工候補生成
  - 好みに忠実
  - 鮮明・クリア
  - ノスタルジック
  - ダーク・シネマ
  - 明るい・エアリー
  - 鮮やか・ポップ
- 候補ごとの加工画像・JSON・CSV保存

## 使用技術

- Python 3.12
- NumPy
- Pandas
- Pillow
- Matplotlib
- Streamlit
- pytest
- Ruff
- uv
- GitHub Actions

## セットアップ

### 1. リポジトリを取得

```bash
git clone https://github.com/ShunNishida0701/Prog.git
cd Prog

```

### 2. uvをインストール

LinuxまたはGitHub Codespacesの場合：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

ターミナルを開き直し、確認します。

```bash
uv --version
```

### 3. 依存関係をインストール

```bash
uv sync --locked --dev
```

## アプリの起動

```bash
uv run streamlit run streamlit_app.py
```

表示されたURLをブラウザで開きます。

GitHub Codespacesでは、ポート`8501`をブラウザで開きます。

## 使い方

1. 好みのJPEG・PNG画像を複数アップロードします。
2. 写真ごとの明るさ、コントラスト、彩度を確認します。
3. 好みの平均プロファイルを確認します。
4. 加工対象写真を1枚アップロードします。
5. 6種類の加工候補をタブで比較します。
6. 好みに近い候補を選びます。
7. 選んだ加工画像をPNGまたはJPEGで保存します。
8. 加工レシピをJSONまたはCSVで保存します。

## テスト

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## プロジェクト構成

```text
Prog/
├── src/
│   └── my_color_recipe_ai/
│       ├── __init__.py
│       ├── image_features.py
│       ├── image_processing.py
│       ├── preference.py
│       ├── recipe.py
│       ├── storage.py
│       └── variations.py
├── tests/
│   ├── test_image_features.py
│   ├── test_image_processing.py
│   ├── test_preference.py
│   ├── test_recipe.py
│   ├── test_storage.py
│   ├── test_streamlit_app.py
│   └── test_variations.py
├── .github/
│   └── workflows/
│       └── test.yml
├── outputs/
│   └── .gitkeep
├── sample_images/
│   └── README.md
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

## 現在の計算方法

- 明るさ：RGB値から計算した輝度の平均
- コントラスト：輝度の標準偏差
- 彩度：各画素のRGB最大値と最小値の差
- 加工レシピ：好みの平均特徴量と加工対象写真の特徴量との差

## 制限事項

- 現在扱う特徴量は明るさ、コントラスト、彩度の3種類です。
- 加工値は単純な特徴量差から計算しています。
- 加工後の特徴量が好みの平均へ完全一致するとは限りません。
- 被写体や撮影条件の違いは考慮していません。
- 高度な機械学習による最適化は今後の改善候補です。

## AIの利用について

開発ではAIを、機能設計、関数単位のコード案、テスト案、エラー調査、コードレビュー、CIおよび文書構成の提案に使用しました。

AIの提案は、pytest、Ruff、GitHub Actionsおよび実際の画面操作によって確認しました。最終的な採用判断と目視確認は自分で行いました。

## ライセンス

このプロジェクトはMIT Licenseで公開しています。