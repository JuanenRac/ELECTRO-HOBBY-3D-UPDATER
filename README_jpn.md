<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <b>🇯🇵 日本語</b>
</p>

### Electro Hobby 3D の3つのエコシステム全てに対応する単一のコマンドライン - システムを選び、そのパッケージをダウンロード・更新する

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**正直さのチェック - 今日動いているもの:** **成熟度:骨組み。** これはエコシステム発見の4つ目の実装ではなく、薄いディスパッチャーです。マニフェスト解析、インストール、更新の独自ロジックは一切持ちません。`dispatch()` とそのコマンド構築(偽のサブプロセスランナーに対する16件のテスト)は実際にテスト済みです。`status --ecosystem all` は3つのエコシステム全ての実際のチェックアウトに対して実際に実行され(HYDRA-UMC 55件、URTC 7件、A.R.M.O.R. 17件のリポジトリを正しく検出)、`install`/`update` はまだです。その最初の実行で実際のバグが発見・修正されました:`CHANGELOG.md` の `--workspace` の項目を参照してください。

---

## 🎯 概要

* **1 つのツールで 3 つの実エコシステム：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) にはそれぞれ独立してテストされた専用アップデーターがあります。このプロジェクトはそれらを再実装せず、3 つを実際の依存関係としてインストールし、`--ecosystem hydra-umc|urtc|armor` を該当するものへ振り分けます。
* **固定され、レビュー済みの依存関係：** `pyproject.toml` は各サブアップデーターを、動き続ける `main` ではなくレビュー済みのコミットに固定するため、インストールでは常にレビューした内容そのものが入ります。`versions` は各アップデーターのインストール済みバージョンを表示し、GitHub より古いものを知らせます。
* **毎回、実際の独立したサブプロセス。** 各呼び出しは `python -m <そのエコシステムのモジュール> --cli ...` を独自のインタープリターで実行し、他の CLI の `main()` をこのプロセスにインポートすることはありません。`sys.argv` を読み `sys.exit()` を呼ぶ 3 つの独立した argparse プログラムは、同じプロセスでは互いに壊し合ってしまいます。
* **`status --ecosystem all`：** 3 つのエコシステムのステータス確認を同時に実行し、各レポートを固定の順序でまとめて出力し、最初の失敗で止まらずにどれが失敗したかを示します。
* **`install`/`update` には常に 1 つのエコシステムと 1 つのプロジェクト名が必要です。** ここには「全エコシステムをすべて更新」はなく、各サブアップデーターの CLI と同じ方針です。
* **引き継がれる制限：** このツールは各サブアップデーターの動作をそのまま実行します。A.R.M.O.R. のアップデーターは自分自身を更新すると、まだ自身のインストールを壊します（編集可能インストールがステージングディレクトリを指したままになる）ので、当面 ARMOR-UPDATER は手動で更新してください。URTC-UPDATER は署名付きコミットを必須にできます（`URTC_UPDATER_REQUIRE_SIGNED=1`）が、他の 2 つはまだ署名を検証しません。

## 📂 リポジトリ構造

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # 3つの実在するエコシステムとその CLI モジュールを唯一名指しする場所
│   ├── main.py         # argparse CLI + dispatch() - 正しいサブプロセスコマンドを構築して実行する
│   ├── i18n.py         # ウィンドウの文言（7言語）
│   ├── qt_gui.py       # Qt Quick ウィンドウ（エコシステムごとのカードとログ）- 各エコシステム専用のアップデーターを開く
│   └── qml/Main.qml    # ウィンドウの QML
├── tests/               # 偽のサブプロセスランナーに対する16件のテスト
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + 編集可能インストール(3つの実際の依存関係を取得) + コンパイルチェック
├── build-test.sh / build-test.bat  # 同じインストールの後、実際の pytest スイート
└── run.sh / run.bat              # CLI エントリーポイント（引数なし: ウィンドウ）
```

## 🛠️ 開発環境

```bash
pip install -e ".[dev]"                 # GitHub から hydra-umc-updater、urtc-updater、armor-updater もインストールする
python -m pytest tests -q               # 16件のテスト、ネットワークも実際のサブプロセスも不要
electro-hobby-3d-updater status --ecosystem all               # 全エコシステムを並列にチェックする
electro-hobby-3d-updater versions                             # 各アップデーターのインストール済みバージョンと GitHub より古いかどうか
electro-hobby-3d-updater status --ecosystem armor             # 1つだけチェックする
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # まだインストールされていないプロジェクトをクローンしてビルドする
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # 既にインストール済みのプロジェクトをプルして再ビルドする
```

## 🔗 関連プロジェクト

このツールは JuanenRac (Electro Hobby 3D) 自身のアップデーターファミリーの4つ目のピースです - 他のどれかを置き換えるのではなく、その3つをラップします:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - HYDRA-UMC エコシステム自身のリポジトリを検出・インストール・更新する
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - URTC エコシステム自身のリポジトリを検出・インストール・更新する
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - A.R.M.O.R. エコシステム自身のリポジトリを検出・インストール・更新する
* **ELECTRO-HOBBY-3D-UPDATER** (本リポジトリ) - ユーザーが選んだ3つのうちの1つへディスパッチする

そして3つの実在するエコシステム自体: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (産業用マルチロボット制御), **[URTC](https://github.com/JuanenRac/URTC)** (Universal Robot Tool Controller プラットフォーム), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (境界防犯とホームオートメーション).

## 📚 ドキュメントとコミュニティ

* **[本リポジトリの変更履歴](CHANGELOG.md)**
* 質問、アイデア、報告: electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

GPL-3.0-or-later - 詳細は [LICENSE](LICENSE).
