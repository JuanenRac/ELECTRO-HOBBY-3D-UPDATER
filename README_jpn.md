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
  <b>🇯🇵 日本語</b> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### Electro Hobby 3D の4つのエコシステム全てに対応する単一のコマンドライン - システムを選び、そのパッケージをダウンロード・更新する

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**正直さのチェック - 今日動いているもの:** **成熟度:機能段階(functional)。** これはエコシステム発見の5つ目の実装ではなく、薄いディスパッチャーです。マニフェスト解析、インストール、更新の独自ロジックは一切持ちません。`dispatch()` とそのコマンド構築(偽のサブプロセスランナーに対する19件のテスト)は実際にテスト済みです。`status --ecosystem all` は3つのエコシステム全ての実際のチェックアウトに対して実際に実行され(HYDRA-UMC 55件、URTC 7件、A.R.M.O.R. 17件のリポジトリを正しく検出)、`install` もクリーンな環境から実際に実行し、ARMOR-COMMON を ARMOR アップデーターがクローン・ビルド・テスト・昇格しました(署名のないリビジョンは警告付きでインストールされます)。`update` はまだ実際には実行していません。その最初の実行で実際のバグが発見・修正されました:`CHANGELOG.md` の `--workspace` の項目を参照してください。 EH3D のアップデーターは自身のテスト（317 件、偽の GitHub を使用）から追加されたもので、このディスパッチャー経由での実際のチェックアウトに対する実行はまだ行っていません。

---

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.1.1` |
| 成熟度 | 機能する |
| 技術 | Python 3.10+ / hydra-umc-updater / urtc-updater / eh3d-updater / armor-updater |
| 対象 | 利用者の PC |
| 実機での確認 | 対象外：ここにあるものはハードウェア上では動きません |

## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| ソフトウェア | 🟡 | 薄いディスパッチャーです。探索・インストール・更新の独自ロジックはなく、`--ecosystem hydra-umc\|urtc\|armor\|eh3d` を各エコシステムのアップデーターに渡します。アップデーターは固定した依存関係としてインストールされます。 |
| テスト | 🟢 | 19 件のテストが、ディスパッチと組み立てるコマンドを確認しています。いずれも模擬のサブプロセス実行器を使います。 |
| 実運用 | 🟠 | `status` は古い 3 つのエコシステムの実際のチェックアウトに対して実行済みで、`install` はクリーンな環境から 1 回実行しました。`update` は実際には実行していません。 |
| 連携 | 🟠 | EH3D アップデーターへの引き渡しは、そのアップデーター自身のテストに基づいて追加されたもので、このディスパッチャー経由で実際のチェックアウトに対して実行したことはありません。 |
| セキュリティ | 🟡 | 各サブアップデーターはレビュー済みのコミットに固定され、動く可能性のあるブランチには固定されません。署名のないリビジョンは警告付きでインストールされ、独立したレビューは受けていません。 |
| 実機 | 🟢 | 該当なし：使う人の PC 上で動作します。 |
| ドキュメント | 🟢 | 8 言語の README。変更のたびにマニフェストと変更履歴との整合を確認しています。 |

## 🎯 概要

* **1 つのツールで 4 つの実エコシステム：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER)、[EH3D](https://github.com/JuanenRac/EH3D-UPDATER) にはそれぞれ独立してテストされた専用アップデーターがあります。このプロジェクトはそれらを再実装せず、4 つを実際の依存関係としてインストールし、`--ecosystem hydra-umc|urtc|armor` を該当するものへ振り分けます。
* **固定され、レビュー済みの依存関係：** `pyproject.toml` は各サブアップデーターを、動き続ける `main` ではなくレビュー済みのコミットに固定するため、インストールでは常にレビューした内容そのものが入ります。`versions` は各アップデーターのインストール済みバージョンを表示し、GitHub より古いものを知らせます。
* **毎回、実際の独立したサブプロセス。** 各呼び出しは `python -m <そのエコシステムのモジュール> --cli ...` を独自のインタープリターで実行し、他の CLI の `main()` をこのプロセスにインポートすることはありません。`sys.argv` を読み `sys.exit()` を呼ぶ 4 つの独立した argparse プログラムは、同じプロセスでは互いに壊し合ってしまいます。
* **`status --ecosystem all`：** 4 つのエコシステムのステータス確認を同時に実行し、各レポートを固定の順序でまとめて出力し、最初の失敗で止まらずにどれが失敗したかを示します。
* **`install`/`update` には常に 1 つのエコシステムと 1 つのプロジェクト名が必要です。** ここには「全エコシステムをすべて更新」はなく、各サブアップデーターの CLI と同じ方針です。
* **引き継がれる制限：** このツールは各サブアップデーターの動作をそのまま実行します。A.R.M.O.R. のアップデーターは自分自身を更新すると、まだ自身のインストールを壊します（編集可能インストールがステージングディレクトリを指したままになる）ので、当面 ARMOR-UPDATER は手動で更新してください。URTC-UPDATER は署名付きコミットを必須にできます（`URTC_UPDATER_REQUIRE_SIGNED=1`）が、他の 2 つはまだ署名を検証しません。

## 📂 リポジトリ構造

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # 4つの実在するエコシステムとその CLI モジュールを唯一名指しする場所
│   ├── main.py         # argparse CLI + dispatch() - 正しいサブプロセスコマンドを構築して実行する
│   ├── i18n.py         # ウィンドウの文言（8言語）
│   ├── qt_gui.py       # Qt Quick ウィンドウ（エコシステムごとのカードとログ）- 各エコシステム専用のアップデーターを開く
│   └── qml/Main.qml    # ウィンドウの QML
├── tests/               # 偽のサブプロセスランナーに対する19件のテスト
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + 編集可能インストール(4つの実際の依存関係を取得) + コンパイルチェック
├── build-test.sh / build-test.bat  # 同じインストールの後、実際の pytest スイート
└── run.sh / run.bat              # CLI エントリーポイント（引数なし: ウィンドウ）
```

## 🛠️ 開発環境

```bash
pip install -e ".[dev]"                 # GitHub から hydra-umc-updater、urtc-updater、armor-updater、eh3d-updater もインストールする
python -m pytest tests -q               # 19件のテスト、ネットワークも実際のサブプロセスも不要
electro-hobby-3d-updater status --ecosystem all               # 全エコシステムを並列にチェックする
electro-hobby-3d-updater versions                             # 各アップデーターのインストール済みバージョンと GitHub より古いかどうか
electro-hobby-3d-updater status --ecosystem armor             # 1つだけチェックする
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # まだインストールされていないプロジェクトをクローンしてビルドする
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # 既にインストール済みのプロジェクトをプルして再ビルドする
```

## 🔗 関連プロジェクト

このツールは JuanenRac (Electro Hobby 3D) 自身のアップデーターファミリーの5つ目のピースです - 他のどれかを置き換えるのではなく、その4つをラップします:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - HYDRA-UMC エコシステム自身のリポジトリを検出・インストール・更新する
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - URTC エコシステム自身のリポジトリを検出・インストール・更新する
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - A.R.M.O.R. エコシステム自身のリポジトリを検出・インストール・更新する
* **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** - EH3D エコシステム自身のリポジトリを検出・インストール・更新する
* **ELECTRO-HOBBY-3D-UPDATER** (本リポジトリ) - ユーザーが選んだ4つのうちの1つへディスパッチする

そして4つの実在するエコシステム自体: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (産業用マルチロボット制御), **[URTC](https://github.com/JuanenRac/URTC)** (Universal Robot Tool Controller プラットフォーム), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (境界防犯とホームオートメーション), **[EH3D](https://github.com/JuanenRac/EH3D)** (ファブリケーションスイート: CAM、CNC、機械制御).

## 📚 ドキュメントとコミュニティ

* **[本リポジトリの変更履歴](CHANGELOG.md)**
* 質問、アイデア、報告: electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

GPL-3.0-or-later - 詳細は [LICENSE](LICENSE).
