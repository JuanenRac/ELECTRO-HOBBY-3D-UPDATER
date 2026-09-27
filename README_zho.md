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
  <a href="README_jpn.md">🇯🇵 日本語</a>
</p>

### 面向 Electro Hobby 3D 全部三个生态系统的统一命令行——选择一个系统，下载并更新它的软件包

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-10-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-ff9800.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分:** **成熟度：脚手架。** 这是一个轻量的分发器，而不是生态系统发现的第四套实现：它自身不包含任何清单解析、安装或更新逻辑。`dispatch()` 及其命令构建（10 个测试，全部针对模拟的子进程执行器）是真实且经过测试的；`status --ecosystem all` 已经针对三个生态系统的真实检出真正运行过（正确找到 55 个 HYDRA-UMC、7 个 URTC 和 15 个 A.R.M.O.R. 仓库）——`install`/`update` 尚未如此。在那次首次真实运行中发现并修复了一个真实的缺陷：见 `CHANGELOG.md` 中的 `--workspace` 条目。

---

## 🎯 概览

* **一个工具，三个真实生态系统：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER) 和 [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) 各自已经拥有独立且经过测试的专属更新器。本项目不重新实现其中任何一个——它把这三者作为真实依赖安装（直接来自各自的 GitHub 仓库），并将 `--ecosystem hydra-umc|urtc|armor` 分发到对应的那一个。
* **每次都是真实、独立的子进程。** 每次调用都以独立的解释器进程运行 `python -m <该生态系统的模块> --cli ...`——绝不会把另一个 CLI 的 `main()` 导入到同一个进程中。三个独立的 argparse 程序，各自可以读取 `sys.argv` 并调用 `sys.exit()`，如果在同一进程中组合会相互破坏；子进程提供了与一个人手动逐条输入命令相同的隔离性。
* **`status --ecosystem all`：** 这是唯一一件单个子更新器自己做不到的事——按顺序运行三个生态系统各自的状态检查，并报告哪个（些）失败了，而不会在第一个失败时就停止。
* **`install`/`update` 始终需要一个生态系统和一个项目名称。** 这里不存在"跨所有生态系统全部更新"这种操作，这与每个子更新器自身 CLI 对其自己项目已经采取的不可协商立场一致。

## 📂 仓库结构

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # 唯一命名三个真实生态系统及其 CLI 模块的地方
│   └── main.py         # argparse CLI + dispatch() —— 构建并运行正确的子进程命令
├── tests/               # 10 个测试，针对模拟的子进程执行器
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # 创建虚拟环境 + 可编辑安装（拉取 3 个真实依赖）+ 编译检查
├── build-test.sh / build-test.bat  # 相同的安装步骤，然后运行真实的 pytest 套件
└── run.sh / run.bat              # CLI 入口点
```

## 🛠️ 开发环境

```bash
pip install -e ".[dev]"                 # 同时会从 GitHub 安装 hydra-umc-updater、urtc-updater 和 armor-updater
python -m pytest tests -q               # 10 个测试，不需要网络或真实子进程
electro-hobby-3d-updater status --ecosystem all               # 按顺序检查全部三个生态系统
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
