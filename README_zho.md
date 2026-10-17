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
  <b>🇨🇳 简体中文</b> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <a href="README_por.md">🇵🇹 Português</a>
</p>

### 面向 Electro Hobby 3D 全部三个生态系统的统一命令行——选择一个系统，下载并更新它的软件包

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分:** **成熟度：可用（functional）。** 这是一个轻量的分发器，而不是生态系统发现的第四套实现：它自身不包含任何清单解析、安装或更新逻辑。`dispatch()` 及其命令构建（16 个测试，全部针对模拟的子进程执行器）是真实且经过测试的；`status --ecosystem all` 已经针对三个生态系统的真实检出真正运行过（正确找到 55 个 HYDRA-UMC、7 个 URTC 和 17 个 A.R.M.O.R. 仓库）——`install` 也已在干净环境中真实运行：ARMOR-COMMON 由 ARMOR 更新器克隆、构建、测试并提升（未签名的修订会带警告安装）；`update` 尚未真实运行。在那次首次真实运行中发现并修复了一个真实的缺陷：见 `CHANGELOG.md` 中的 `--workspace` 条目。

---

## 🎯 概览

* **一个工具，三个真实生态系统：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER) 和 [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) 各自已有独立测试过的专用更新器。本项目不重新实现其中任何部分：它把三者作为真实依赖安装，并将 `--ecosystem hydra-umc|urtc|armor` 分发给对应的更新器。
* **固定且经过审查的依赖：** `pyproject.toml` 把每个子更新器固定到一个审查过的提交，而不是不断变化的 `main`，因此安装得到的始终正是审查过的内容。`versions` 显示每个更新器的已安装版本，并提示哪个落后于 GitHub。
* **每次都是真实、独立的子进程。** 每次调用都在独立的解释器中运行 `python -m <该生态系统的模块> --cli ...`，从不把另一个 CLI 的 `main()` 导入本进程。三个各自读取 `sys.argv`、调用 `sys.exit()` 的独立 argparse 程序在同一进程中会相互破坏。
* **`status --ecosystem all`：** 同时运行三个生态系统的状态检查，按固定顺序完整输出每份报告，并指出哪些失败，而不会在第一个失败处停止。
* **`install`/`update` 总是需要一个生态系统和一个项目名。** 这里没有“更新所有生态系统中的一切”，与每个子更新器自身 CLI 的立场相同。
* **继承的限制：** 本工具执行的就是各子更新器所做的事。A.R.M.O.R. 的更新器在更新自身时仍会破坏自己的安装（可编辑安装指向其暂存目录），因此目前请手动更新 ARMOR-UPDATER。URTC-UPDATER 可以要求签名提交（`URTC_UPDATER_REQUIRE_SIGNED=1`）；另外两个尚未验证签名。

## 📂 仓库结构

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # 唯一命名三个真实生态系统及其 CLI 模块的地方
│   ├── main.py         # argparse CLI + dispatch() —— 构建并运行正确的子进程命令
│   ├── i18n.py         # 窗口文字（八种语言）
│   ├── qt_gui.py       # Qt Quick 窗口（每个生态系统一张卡片、一个日志）—— 打开各生态系统自己的更新器
│   └── qml/Main.qml    # 窗口的 QML
├── tests/               # 16 个测试，针对模拟的子进程执行器
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # 创建虚拟环境 + 可编辑安装（拉取 3 个真实依赖）+ 编译检查
├── build-test.sh / build-test.bat  # 相同的安装步骤，然后运行真实的 pytest 套件
└── run.sh / run.bat              # CLI 入口点（无参数：打开窗口）
```

## 🛠️ 开发环境

```bash
pip install -e ".[dev]"                 # 同时会从 GitHub 安装 hydra-umc-updater、urtc-updater 和 armor-updater
python -m pytest tests -q               # 16 个测试，不需要网络或真实子进程
electro-hobby-3d-updater status --ecosystem all               # 检查全部生态系统（并行）
electro-hobby-3d-updater versions                             # 每个更新器的已安装版本，以及是否落后于 GitHub
electro-hobby-3d-updater status --ecosystem armor             # 只检查一个
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # 克隆并构建一个尚未安装的项目
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # 拉取并重新构建一个已安装的项目
```

## 🔗 相关项目

本工具是 JuanenRac（Electro Hobby 3D）自己的更新器家族中的第四件作品——它包裹了另外三个，而不是取代其中任何一个：

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - 检测、安装并更新 HYDRA-UMC 生态系统自身的仓库
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - 检测、安装并更新 URTC 生态系统自身的仓库
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - 检测、安装并更新 A.R.M.O.R. 生态系统自身的仓库
* **ELECTRO-HOBBY-3D-UPDATER** (本仓库) - 分发到用户选择的三者之一

以及三个真实的生态系统本身： **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (工业多机器人控制), **[URTC](https://github.com/JuanenRac/URTC)** (通用机器人工具控制器平台), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (周界安防与家庭自动化).

## 📚 文档与社区

* **[本仓库的更新日志](CHANGELOG.md)**
* 问题、想法与报告: electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

GPL-3.0-or-later - 详见 [LICENSE](LICENSE).
