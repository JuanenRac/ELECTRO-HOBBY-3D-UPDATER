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
  <img src="https://img.shields.io/badge/Tests-10-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**正直さのチェック - 今日動いているもの:** **成熟度:骨組み。** これはエコシステム発見の4つ目の実装ではなく、薄いディスパッチャーです。マニフェスト解析、インストール、更新の独自ロジックは一切持ちません。`dispatch()` とそのコマンド構築(偽のサブプロセスランナーに対する10件のテスト)は実際にテスト済みです。`status --ecosystem all` は3つのエコシステム全ての実際のチェックアウトに対して実際に実行され(HYDRA-UMC 55件、URTC 7件、A.R.M.O.R. 15件のリポジトリを正しく検出)、`install`/`update` はまだです。その最初の実行で実際のバグが発見・修正されました:`CHANGELOG.md` の `--workspace` の項目を参照してください。

---

## 🎯 概要

* **1つのツール、3つの実在するエコシステム:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) はそれぞれ既に独自の、独立してテストされたアップデーターを持っています。このプロジェクトはそれらを一切再実装しません - 3つ全てを実際の依存関係として(それぞれの GitHub リポジトリから直接)インストールし、`--ecosystem hydra-umc|urtc|armor` を対応するものへディスパッチします。
* **毎回、実際に独立したサブプロセス。** 各呼び出しは `python -m <そのエコシステムのモジュール> --cli ...` を独自のインタープリタープロセスとして実行します - 別の CLI の `main()` を同じプロセスにインポートすることは決してありません。それぞれ独自に `sys.argv` を読み、`sys.exit()` を呼び出せる3つの独立した argparse プログラムを同一プロセス内で組み合わせると、互いを壊してしまいます。サブプロセスは、人が各コマンドを手動で入力するのと同じ分離を提供します。
* **`status --ecosystem all`:** 単一のサブアップデーターだけでは実現できない、このツールならではの機能 - 3つのエコシステム全ての状態チェックを順番に実行し、最初の失敗で止まることなく、どれが失敗したかを報告します。
* **`install`/`update` は常に1つのエコシステムと1つのプロジェクト名を必要とします。** 「全エコシステムにわたって全てを更新する」という操作はここには存在しません。これは各サブアップデーター自身の CLI が既に自分のプロジェクトに対して取っている、譲れない姿勢と同じです。

## 📂 リポジトリ構造

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # 3つの実在するエコシステムとその CLI モジュールを唯一名指しする場所
│   ├── main.py         # argparse CLI + dispatch() - 正しいサブプロセスコマンドを構築して実行する
│   ├── i18n.py         # ウィンドウの文言（7言語）
│   ├── qt_gui.py       # Qt Quick ウィンドウ（エコシステムごとのカードとログ）- 各エコシステム専用のアップデーターを開く
│   └── qml/Main.qml    # ウィンドウの QML
├── tests/               # 偽のサブプロセスランナーに対する12件のテスト
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + 編集可能インストール(3つの実際の依存関係を取得) + コンパイルチェック
├── build-test.sh / build-test.bat  # 同じインストールの後、実際の pytest スイート
└── run.sh / run.bat              # CLI エントリーポイント（引数なし: ウィンドウ）
```

## 🛠️ 開発環境

```bash
pip install -e ".[dev]"                 # GitHub から hydra-umc-updater、urtc-updater、armor-updater もインストールする
python -m pytest tests -q               # 10件のテスト、ネットワークも実際のサブプロセスも不要
electro-hobby-3d-updater status --ecosystem all               # 3つのエコシステムを順番にチェックする
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
