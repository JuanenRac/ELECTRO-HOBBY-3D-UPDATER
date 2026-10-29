<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### Electro Hobby 3D の 4 つのエコシステムすべてに対する 1 つのコマンドラインと 1 つのウィンドウ：システムを選び、そのシステムがすでに持つ更新ツールでパッケージをダウンロード・更新します

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**正直さの確認 - 今日実際に動くもの：** これは薄いディスパッチャーで、エコシステム検出の 5 つ目の実装ではありません。マニフェストの解析、インストール、更新の独自ロジックは持ちません。4 つのエコシステムにはそれぞれ専用の更新ツールがあり、各リポジトリの `<エコシステム>.project.json` マニフェストでプロジェクトを見つけます。このツールは 4 つを固定された依存関係としてインストールし、選んだものを別プロセスとして実行します（`status` は 4 つを同時に）。ディスパッチと組み立てるコマンドはテスト済みです（偽のプロセス ランナーで 18 件が通ります）。`status --ecosystem all` は 3 つのエコシステムの実際のチェックアウトに対して実際に実行し、`install` はクリーンな環境から 1 回実行しました（A.R.M.O.R. の更新ツールが 1 つのプロジェクトをクローン、ビルド、テストして反映）。`update` は実際には実行しておらず、EH3D 更新ツールへの引き渡しはその更新ツール自身のテストから追加したもので、このツール経由で実際のチェックアウトに対して実行したことはありません。

---

> **安全性とセキュリティの現状：** 実行する更新ツールを通して自分のマシン上のファイルを置き換えるため、各ツールが行うこと以上のことはせず、1 度に 1 つのプロジェクトを、その更新ツールが求める確認のあとに処理します。勝手には何も実行せず、「エコシステム全体をまとめて更新」することも決してなく、機械は制御しません。各更新ツールは動くブランチではなくレビュー済みのコミットに固定されています。未署名のリビジョンは、その更新ツールが署名を必須にしていない限り、警告付きでインストールされます。

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.1.1` |
| 成熟度 | 機能する |
| テスト | 18 |
| 技術スタック | Python 3.10+ (PySide6 for the window) |
| 実機での動作 | 該当なし：使う人の PC 上で動きます |

**移動先：** [概要](#-概要) · [アーキテクチャ](#-アーキテクチャ) · [クイックスタート](#-クイックスタート) · [テスト](#-テスト) · [構成](#-リポジトリの構成) · [関連](#-関連プロジェクト)

## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| ソフトウェア | 🟡 | 薄いディスパッチャーです。独自の検出・インストール・更新ロジックを持たず、`--ecosystem hydra-umc\|urtc\|armor\|eh3d` を各エコシステムの更新ツールへ引き渡します。更新ツールは固定された依存関係としてインストールされます。 |
| テスト | 🟢 | 偽のプロセス ランナーに対して 18 件のテストが通ります（`pytest`）。PySide6 が未インストールの場合は、もう 1 件がスキップされます。 |
| 実使用 | 🟠 | `status` は 3 つのエコシステムの実際のチェックアウトに対して、`install` はクリーンな環境から 1 回実行しました。`update` は実際には実行していません。 |
| ウィンドウ | 🟡 | ウィンドウ（エコシステムごとのカード、ログ、8 言語）は各エコシステム自身の更新ツールを開きます。文言とスレッドの規則はテスト済みで、残りは手作業の確認のみです。 |
| 連携 | 🟠 | EH3D 更新ツールへの引き渡しはその更新ツール自身のテストから追加したもので、このディスパッチャー経由で実際のチェックアウトに対して実行したことはありません。 |
| セキュリティ | 🟡 | 各サブ更新ツールは動くブランチではなくレビュー済みのコミットに固定され、実行はそれぞれ時間制限付きの別プロセスです。未署名のリビジョンは警告付きでインストールされ、独立したレビューは受けていません。 |
| 実機 | 🟢 | 該当なし：使う人の PC 上で動きます。 |
| ドキュメント | 🟢 | 8 言語の README。変更のたびにマニフェストと変更履歴と照合します。 |

## 🎯 概要

* **1 つのツール、4 つのエコシステム：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER)、[EH3D](https://github.com/JuanenRac/EH3D-UPDATER) にはそれぞれ独立してテストされた専用の更新ツールがあります。このプロジェクトはそれらを再実装せず、4 つを依存関係としてインストールし、`--ecosystem hydra-umc|urtc|armor|eh3d` を該当するものへ引き渡します。
* **検出は各更新ツールの役目：** 各エコシステムは、各リポジトリのマニフェスト（`hydra-umc.project.json`、`urtc.project.json`、`armor.project.json`、`eh3d.project.json`）でプロジェクトを見つけます。新しいリポジトリはマニフェストを持つだけで自分のエコシステムに現れ、このツールにプロジェクトの一覧はありません。このツール自身のマニフェスト `electro-hobby-3d.project.json` は、設計上 4 つのどれにも属しません。
* **固定されレビュー済みの依存関係：** `pyproject.toml` は各更新ツールをレビュー済みのコミットに固定し、動く `main` には固定しません。`versions` は各更新ツールのインストール済みバージョンを示し、GitHub より古いものに印を付けます。
* **毎回別プロセス：** 各呼び出しは `python -m <そのエコシステムのモジュール> --cli ...` を独立したインタープリターとして実行します。それぞれ `sys.exit()` を呼びうる 4 つの argparse プログラムを 1 つのプロセスに組み合わせると互いに干渉します。
* **`status --ecosystem all`：** 4 つの状態確認を同時に実行し、各レポートを固定の順序で全文表示し、最初で止まらずにどれが失敗したかを報告します。
* **`install` と `update` は常に 1 つのエコシステムと 1 つのプロジェクト名が必要：** 「全エコシステムをまとめて更新」はなく、各更新ツールと同じ方針です。
* **ウィンドウ：** 引数なしで起動すると、Qt Quick ウィンドウがエコシステムごとのカードとログを表示し、各エコシステム自身の更新ツールを開いて状態を尋ねます（8 言語）。

## 🧩 Electro Hobby 3D での役割

ELECTRO-HOBBY-3D-UPDATER は Electro Hobby 3D の更新ツール ファミリーの 5 つ目で、4 つのエコシステムの上に位置します。他の 4 つを置き換えるのではなく包み込みます。複数のエコシステムを扱う人が、すべてを見て更新するものを選べる唯一の場所です。

## 🏛️ アーキテクチャ

<p align="center">
  <img src="images/architecture.svg" alt="ELECTRO-HOBBY-3D-UPDATER のアーキテクチャ：誰が使い、何を持ち、何に依存するか" width="100%">
</p>

このリポジトリの各部分の関係：誰が使い、何を持ち、何に依存するか。図は `docs/architecture.json` から描かれ、コードと照合されます。

## 🔒 セキュリティと安全

| 脅威 | 防御 |
|---|---|
| 更新ツールの動く、または侵害された `main` がこのツールに届く | 各更新ツールは `pyproject.toml` でブランチではなくレビュー済みのコミットに固定されます。新しいものへ移るには、先にレビューしてからここの固定を変更します |
| ある更新ツールが別の更新ツールを壊す | 各呼び出しは更新ツールを独立したインタープリター プロセス（`python -m <モジュール> --cli ...`）として実行し、このプロセスには決してインポートしないため、他の引数・状態・終了を変えられません |
| 固まる更新ツール（git の資格情報待ち、通信断） | すべての実行に時間制限があります。`status` は 900 秒、`install` と `update` は 1800 秒で、`--timeout-seconds` で変更できます（0 は無制限） |
| 望まない一括変更 | `install` と `update` は 1 つのエコシステムと 1 つのプロジェクト名だけを受け取り、`--ecosystem all` を拒否します。各更新ツールがそれぞれ確認を求めます |
| 違うフォルダーを見てしまう | ワークスペースは常に明示的に転送されます（既定はこのツールの親フォルダー）。そうしないとインストールされた更新ツールがこのツールの仮想環境の下を探し、黙って何も見つけられなくなるためです |
| 出所不明のコミット | 各更新ツールに任されます。署名を必須にするよう指示しない限り、未署名のリビジョンは警告付きでインストールされます（EH3D-UPDATER と URTC-UPDATER にはそのオプションがあります） |
| 1 つのエコシステムの失敗が他を隠す | `status --ecosystem all` は 4 つすべてを実行し、すべてのレポートを表示し、失敗したものの名前を挙げます |

**防御していないこと：** このツールは、各更新ツールが行うことを、あなたの権限で、インストールするプロジェクトのビルド スクリプトを含めて実行します。A.R.M.O.R. の更新ツールは自分自身を更新するとき、まだ自分のインストールを壊すので、ARMOR-UPDATER は手作業で更新してください。ツールは独立したレビューを受けていません。脆弱性は非公開で報告してください（[SECURITY.md](SECURITY.md) 参照）。

## 🔌 インターフェース

| インターフェース | 内容 | 場所 |
|---|---|---|
| コマンドライン | `electro-hobby-3d-updater`：`status`、`install`、`update`、`versions`、`--version`。終了コードは 0、1（実行の失敗または時間切れ）、2（`versions`：更新ツールが GitHub より古い） | `main.py` |
| ウィンドウ | 引数なしで Qt Quick ウィンドウ（エコシステムごとのカードとログ）を開きます。任意の `PySide6` エクストラが必要です | `qt_gui.py`、`qml/Main.qml` |
| 各更新ツールへ | 別プロセス：`python -m <hydra_umc_updater.main、urtc_updater.main、armor_updater.main、eh3d_updater.main のいずれか> --cli <アクション> [プロジェクト] --workspace <フォルダー>` | `ecosystems.py` |
| GitHub | `versions` が、各更新ツールのリポジトリの `main` の `pyproject.toml` を読んでバージョンを比較します。それ以外はありません | `main.py` |

## ⚙️ 設定

設定は不要です。コマンドラインのオプションが設定のすべてで、それ以外は各更新ツールのものです。

| オプション | 既定値 | 範囲 | 内容 |
|---|---|---|---|
| `--ecosystem` | なし | `hydra-umc`、`urtc`、`armor`、`eh3d`。`all` は `status` のみ | どの更新ツールが作業するか |
| `--workspace` | このツールの親フォルダー | フォルダー | 各更新ツールが走査するワークスペース（常に転送されます） |
| `--offline`（`status`、`versions`） | オフ | オンまたはオフ | GitHub の確認を省略 |
| `--timeout-seconds` | `status` は 900、`install` と `update` は 1800 | 秒数。0 以下は無制限 | 終わらない更新ツールを止める |
| 固定（ピン） | `pyproject.toml` の 4 つのコミット | 各更新ツールのレビュー済みコミット | インストールされる更新ツールのコード。新しいものをレビューしてからのみ変更 |

このリリースの固定は、HYDRA-UMC-UPDATER 0.4.8、URTC-UPDATER 0.1.7、ARMOR-UPDATER 0.1.4、EH3D-UPDATER 0.0.1 です。

## 🚀 クイックスタート

Python 3.10 以降が必要です。ウィンドウには PySide6 も必要です。

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

引数なしの `run.bat` / `run.sh` はウィンドウを開きます。`install` と `update` には、そのエコシステムのマニフェストが宣言する綴りのとおり、エコシステム 1 つとプロジェクト名 1 つが必要です。

## 🧪 テスト

テストは 18 件が通ります（`pytest tests`）。PySide6 が未インストールの場合にスキップされるテストがもう 1 件あります。偽のプロセス ランナーに対して、ネットワークも実際のサブプロセスも使わずに動き、次を網羅します：レジストリがちょうど 4 つのエコシステムを持つこと、`status` が正しいモジュールを実行して `--offline` を転送すること、`status --ecosystem all` が各エコシステムを 1 回ずつ同時に実行して順に表示し最初の失敗で止まらないこと、`install` と `update` が 1 つのエコシステムと 1 つのプロジェクトを必要とし `all` を拒否すること、失敗した更新ツールの終了コードを引き継ぐこと、ワークスペースの既定が親フォルダーであること、`versions` がインストール済みバージョンを報告し古い更新ツールに印を付け `--offline` では GitHub に接続しないこと、固まった更新ツールが明確なメッセージで止められ時間制限 0 が無制限を意味すること、ウィンドウの文言が 8 言語すべてにあること。CI は `python tools/ci_validate.py`（マニフェスト、バージョン、変更履歴、README の整合）に続いて、すべてのソースをコンパイルしてテストを実行する `python tools/build_test.py` を実行します。

## 🏗️ ビルドとリリース

バージョンは `pyproject.toml`、`electro-hobby-3d.project.json`、パッケージにあり、各バージョンには [CHANGELOG.md](CHANGELOG.md) の項目があります。`build.sh` / `build.bat` は仮想環境を作り、固定された 4 つの更新ツールとともにこのツールをインストールしてコンパイル検査します。`build-test.sh` / `build-test.bat` は同じことをしてからテストを実行し、`test.sh` / `test.bat` はテストだけを実行します。いずれもライブ パネルで動き、バージョンは変えません。リリースは GitHub で公開されます（最新は 0.1.1）。ツールはこのリポジトリからインストールし、PyPI にはありません。

## 🩺 トラブルシューティング

| 症状 | 対処 |
|---|---|
| あるエコシステムがプロジェクトなしと報告する | 更新ツールは、自分のマニフェストを持つ隣のフォルダーをワークスペースから探します。リポジトリを置いたフォルダーを `--workspace` で指定してください。 |
| `versions` が更新ツールの遅れを示す（終了コード 2） | 固定は意図したものです。その更新ツールの新しいコミットをレビューして `pyproject.toml` に入れ、このツールのバージョンを上げて再インストールしてください。 |
| ウィンドウが開かない | PySide6 が必要です：`pip install -e ".[gui]"`。コマンドラインはなくても動きます。 |
| 更新ツールが長く動きすぎた | 制限（`status` は 900 秒、`install` と `update` は 1800 秒）で止められました。`--timeout-seconds` で延ばすか、0 で無制限にしてください。 |
| ARMOR-UPDATER が自己更新のあとに壊れる | 編集可能インストールがステージング フォルダーを指しています。ARMOR-UPDATER を手作業で更新し、`build.bat` / `build.sh` をもう一度実行してください。 |

## 📂 リポジトリの構成

<p align="center">
  <img src="images/repository-structure.svg" alt="ELECTRO-HOBBY-3D-UPDATER のリポジトリ構成" width="100%">
</p>

<details>
<summary>ツリーのテキスト版</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            4 つのエコシステムの名前を定める唯一の場所
│   ├── main.py                                  コマンドライン、ディスパッチ、バージョン
│   ├── qt_gui.py qml/                           Qt Quick ウィンドウとその QML
│   ├── i18n.py                                  8 言語のウィンドウの文言
│   └── assets/                                  プログラムのアイコン
├── tests/                                       偽のプロセス ランナーに対するディスパッチ
├── docs/                                        アーキテクチャ図と構成図のデータ
├── tools/                                       CI・ビルド・README のチェックと図
├── images/                                      バナーとアーキテクチャ・リポジトリ構成の図
├── .github/                                     CI とリリースのワークフロー、Issue と PR のテンプレート
├── build.sh build.bat                           仮想環境、編集可能インストール、検査をライブ パネルで
├── build-test.sh build-test.bat                 同じことをして、続けて実際のテスト スイート
├── run.sh run.bat                               ウィンドウを起動（引数があればコマンドライン）
├── bump*.py                                     バージョンを上げるスクリプト
├── electro-hobby-3d.project.json                マニフェスト：バージョン、役割、成熟度
├── pyproject.toml                               パッケージと固定された 4 つの更新ツール
├── CHANGELOG.md                                 各バージョンの変更点
├── SECURITY.md SUPPORT.md                       脆弱性の報告方法と問い合わせ先
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   貢献方法、行動規範、ライセンス
```

</details>

## 🗺️ ロードマップと既知の制限

**現時点で分かっている制限**

* `update` は実際には実行しておらず、`install` は 1 回だけです。`status` は 3 つのエコシステムの実際のチェックアウトに対して実行しました。
* EH3D-UPDATER への引き渡しは、このツール経由で実際のチェックアウトに対して実行していません。
* 設計上、「全エコシステムをまとめて更新」はありません。
* コミットの署名を必須にするかどうかは各更新ツールに任されており、A.R.M.O.R. の更新ツールは自己更新のときに自分のインストールを壊します。
* ツールは独立したレビューを受けておらず、PyPI にもありません。

**次のステップ**

* EH3D のプロジェクトの `status`、`install`、`update` を、このツール経由で実際のチェックアウトに対して実行する。
* 4 つの更新ツールが新しいリリースを出すたびに、固定をレビュー済みの新しいコミットへ移す。
* いずれかのエコシステムで `update` を実際に実行し、見つかったことを記録する。

## 🌍 言語

README とテキストは、英語、スペイン語、フランス語、イタリア語、ドイツ語、中国語、日本語、ヨーロッパポルトガル語で提供されています。

## 🔗 関連プロジェクト

このツールは JuanenRac（Electro Hobby 3D）の更新ツール ファミリーの 5 つ目で、他の 4 つを置き換えるのではなく包み込みます。

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)：HYDRA-UMC のリポジトリを検出・インストール・更新
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)：URTC のリポジトリを検出・インストール・更新
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)：A.R.M.O.R. のリポジトリを検出・インストール・更新
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)：EH3D のリポジトリを検出・インストール・更新
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)、[URTC](https://github.com/JuanenRac/URTC)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)、[EH3D](https://github.com/JuanenRac/EH3D-DOCS)：4 つのエコシステムそのもの

## 📚 ドキュメント

* [変更履歴](CHANGELOG.md)：各バージョン、変更点、見つかったこと。
* [コントリビュート](CONTRIBUTING.md)、[セキュリティ ポリシー](SECURITY.md)、[サポート](SUPPORT.md)。
* 各エコシステム自身の更新ツールのドキュメントは、それぞれのリポジトリにあります（関連プロジェクトを参照）。

## 🤝 コントリビュートとコミュニティ

* プルリクエストの前に `python -m pytest tests -q` と `python tools/ci_validate.py` を実行し、どちらも通してください。[CONTRIBUTING.md](CONTRIBUTING.md) と[行動規範](CODE_OF_CONDUCT.md)を参照してください。
* README は 8 言語あります。文章を変更するときは 8 つのファイルすべてを変更し、2 つの図は `docs/architecture.json` と `docs/structure.json` から `tools/make_architecture.py` と `tools/make_structure.py` で描画します。
* このツールはディスパッチャーであり続けなければなりません。検出・インストール・更新のロジックはエコシステムの更新ツールに置き、ここには置きません。新しいエコシステムの追加は `ecosystems.py` の 1 行の変更です。
* 脆弱性は非公開で報告してください：[SECURITY.md](SECURITY.md)。質問、アイデア、報告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later。[LICENSE](LICENSE) を参照。スイートのハードウェア設計には CERN OHL-S を使います。
