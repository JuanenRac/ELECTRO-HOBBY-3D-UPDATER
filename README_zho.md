<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### 面向 Electro Hobby 3D 全部四个生态系统的一个命令行和一个窗口：选择一个系统，通过该系统已有的更新器下载并更新其软件包

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**诚实性核对 - 今天真正能运行的内容：** 这是一个薄的分派器，不是生态系统发现的第五种实现：它没有自己的清单解析、安装或更新逻辑。四个生态系统各有自己的更新器，通过每个仓库的 `<生态系统>.project.json` 清单找到其项目；本工具把这四个作为固定版本的依赖安装，并把你选择的那个作为独立进程运行（`status` 可同时运行四个）。分派及其构造的命令已测试（用模拟的进程运行器，18 个测试通过）。`status --ecosystem all` 已对其中三个生态系统的真实检出实际运行过，`install` 也在干净环境中运行过一次（一个项目由 A.R.M.O.R. 更新器克隆、构建、测试并转正）；`update` 尚未真实运行，对 EH3D 更新器的交接是根据该更新器自己的测试加入的，尚未通过本工具在真实检出上运行过。

---

> **安全（safety）与信息安全现状：** 它通过所运行的更新器来替换你机器上的文件，所以只做每个更新器各自所做的事，一次一个项目，并在该更新器要求的确认之后进行。它不会自行运行任何东西，从不“跨生态系统更新全部”，也不控制任何机床。每个更新器都固定到经过审阅的提交，而不是移动的分支；未签名的修订会带警告安装，除非该更新器被设置为要求签名。

## 📋 速览

| | |
|---|---|
| 版本 | `0.1.1` |
| 成熟度 | 可用 |
| 测试 | 18 |
| 技术栈 | Python 3.10+ (PySide6 for the window) |
| 真实硬件 | 不适用：它运行在使用者的电脑上 |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [快速开始](#-快速开始) · [测试](#-测试) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 软件 | 🟡 | 一个薄的分派器：它没有自己的发现、安装或更新逻辑，把 `--ecosystem hydra-umc\|urtc\|armor\|eh3d` 交给每个生态系统的更新器，这些更新器作为固定版本的依赖被安装。 |
| 测试 | 🟢 | 18 个测试通过（`pytest`），使用模拟的进程运行器；未安装 PySide6 时另有 1 个被跳过。 |
| 真实使用 | 🟠 | `status` 已对其中三个生态系统的真实检出运行过，`install` 在干净环境中运行过一次；`update` 尚未真实运行。 |
| 窗口 | 🟡 | 窗口（每个生态系统一张卡片、一个日志、八种语言）会打开每个生态系统自己的更新器；其文本和线程规则已测试，其余只靠手工检查。 |
| 集成 | 🟠 | 对 EH3D 更新器的交接是根据该更新器自己的测试加入的，尚未通过本分派器在真实检出上运行过。 |
| 安全 | 🟡 | 每个子更新器都固定到经过审阅的提交，而不是移动的分支；每次运行都是带时间限制的独立进程；未签名的修订会带警告安装，也未经独立审查。 |
| 真实硬件 | 🟢 | 不适用：它运行在使用者的电脑上。 |
| 文档 | 🟢 | 八种语言的 README，每次更改都会与清单和变更日志对照。 |

## 🎯 概述

* **一个工具，四个生态系统：** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)、[URTC](https://github.com/JuanenRac/URTC-UPDATER)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) 和 [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) 各有自己的、独立测试过的更新器。本项目不重新实现其中任何一个：它把四个都作为依赖安装，并把 `--ecosystem hydra-umc|urtc|armor|eh3d` 分派给对应的那一个。
* **发现仍由各个更新器负责：** 每个生态系统通过每个仓库的清单（`hydra-umc.project.json`、`urtc.project.json`、`armor.project.json`、`eh3d.project.json`）找到自己的项目，所以新仓库只要有清单就会出现在它的生态系统中，这个工具里没有任何项目列表。本工具自己的清单 `electro-hobby-3d.project.json` 按设计不属于四者中的任何一个。
* **固定且经过审阅的依赖：** `pyproject.toml` 把每个更新器固定到经过审阅的提交，而不是移动的 `main`。`versions` 显示每个更新器已安装的版本，并标出落后于 GitHub 的。
* **每次都是独立进程：** 每次调用都把 `python -m <该生态系统的模块> --cli ...` 作为独立解释器运行；四个都可能调用 `sys.exit()` 的 argparse 程序若放在同一进程中会互相破坏。
* **`status --ecosystem all`：** 同时运行四个状态检查，按固定顺序完整打印每份报告，并说明哪些失败了，而不是在第一个失败处停下。
* **`install` 和 `update` 始终需要一个生态系统和一个项目名称：** 没有“跨所有生态系统更新全部”，与每个更新器的立场相同。
* **窗口：** 不带参数时，Qt Quick 窗口为每个生态系统显示一张卡片和一个日志，打开每个生态系统自己的更新器并询问其状态，支持八种语言。

## 🧩 在 Electro Hobby 3D 中的角色

ELECTRO-HOBBY-3D-UPDATER 是 Electro Hobby 3D 更新器家族的第五个成员，位于四个生态系统之上：它包装另外四个而不是取代其中任何一个。对于同时使用多个生态系统的人来说，这是能看到全部并选择要更新哪个的唯一地方。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="ELECTRO-HOBBY-3D-UPDATER 的架构：谁在使用、包含什么、依赖什么" width="100%">
</p>

本仓库各部分如何协作：谁在使用它、它包含什么、它依赖什么。图片由 `docs/architecture.json` 绘制，并与代码核对。

## 🔒 安全与防护

| 威胁 | 防御 |
|---|---|
| 某个更新器移动或被入侵的 `main` 传到本工具 | 每个更新器在 `pyproject.toml` 中固定到经过审阅的提交，而不是分支；要换到更新的版本，先审阅，再在这里修改固定 |
| 一个更新器干扰另一个 | 每次调用都把更新器作为独立的解释器进程运行（`python -m <模块> --cli ...`），绝不导入到本进程中，因此谁也无法改变另一个的参数、状态或退出 |
| 卡住的更新器（git 在等凭据、网络断了） | 每次运行都有时间限制：`status` 900 秒，`install` 和 `update` 1800 秒，可用 `--timeout-seconds` 修改（0 表示不限） |
| 不想要的批量更改 | `install` 和 `update` 恰好接受一个生态系统和一个项目名称，并拒绝 `--ecosystem all`；每个更新器各自要求确认 |
| 看错文件夹 | 工作区总是被明确转发（默认为本工具的上级文件夹），否则已安装的更新器会去本工具的虚拟环境下查找，并悄悄地什么也找不到 |
| 来源不明的提交 | 交给每个更新器处理：除非告诉该更新器要求签名，否则未签名的修订会带警告安装（EH3D-UPDATER 和 URTC-UPDATER 有此选项） |
| 一个生态系统的失败掩盖其他的 | `status --ecosystem all` 运行全部四个，打印每份报告，并指出失败的那些 |

**没有防御的内容：** 本工具以你的权限执行每个更新器所做的一切，包括你所安装项目的构建脚本；A.R.M.O.R. 的更新器在更新自身时仍会破坏自己的安装，所以请手动更新 ARMOR-UPDATER；该工具也未经独立审查。请私下报告漏洞（见 [SECURITY.md](SECURITY.md)）。

## 🔌 接口

| 接口 | 内容 | 位置 |
|---|---|---|
| 命令行 | `electro-hobby-3d-updater`，含 `status`、`install`、`update` 和 `versions`；`--version`；退出码 0、1（某次运行失败或超时）和 2（`versions`：某个更新器落后于 GitHub） | `main.py` |
| 窗口 | 不带参数时打开 Qt Quick 窗口（每个生态系统一张卡片和一个日志）；需要可选的 `PySide6` 附加项 | `qt_gui.py`、`qml/Main.qml` |
| 通往每个更新器 | 独立进程：`python -m <hydra_umc_updater.main、urtc_updater.main、armor_updater.main 或 eh3d_updater.main> --cli <动作> [项目] --workspace <文件夹>` | `ecosystems.py` |
| GitHub | `versions` 读取每个更新器仓库在 `main` 上的 `pyproject.toml` 来比较版本；仅此而已 | `main.py` |

## ⚙️ 配置

不需要配置；命令行选项就是全部配置，其余都属于各个更新器。

| 选项 | 默认值 | 范围 | 作用 |
|---|---|---|---|
| `--ecosystem` | 无 | `hydra-umc`、`urtc`、`armor` 或 `eh3d`；`all` 仅用于 `status` | 由哪个更新器来工作 |
| `--workspace` | 本工具的上级文件夹 | 一个文件夹 | 每个更新器扫描的工作区（总是被转发） |
| `--offline`（`status`、`versions`） | 关 | 开或关 | 跳过 GitHub 检查 |
| `--timeout-seconds` | `status` 为 900，`install` 和 `update` 为 1800 | 秒数；0 或更小表示不限 | 停止没有完成的更新器 |
| 固定版本（pin） | `pyproject.toml` 中的四个提交 | 每个更新器经过审阅的提交 | 安装哪份更新器代码；只有审阅过更新的版本后才会更改 |

本版本的固定为 HYDRA-UMC-UPDATER 0.4.8、URTC-UPDATER 0.1.7、ARMOR-UPDATER 0.1.4 和 EH3D-UPDATER 0.0.1。

## 🚀 快速开始

需要 Python 3.10 或更高版本；窗口还需要 PySide6。

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

不带参数的 `run.bat` / `run.sh` 会打开窗口。`install` 和 `update` 需要一个生态系统和一个项目名称，写法与该生态系统的清单所声明的一致。

## 🧪 测试

测试共 18 个通过（`pytest tests`），另有 1 个在未安装 PySide6 时被跳过。它们使用模拟的进程运行器，不联网也不启动真实子进程，覆盖：注册表恰好包含四个生态系统；`status` 运行正确的模块并转发 `--offline`；`status --ecosystem all` 把每个生态系统各运行一次、同时运行、按顺序打印并且不会在第一个失败处停止；`install` 和 `update` 需要一个生态系统和一个项目并拒绝 `all`；失败的更新器会传递它自己的退出码；工作区默认是上级文件夹；`versions` 报告已安装的版本、标出落后的更新器，并且在 `--offline` 时从不联系 GitHub；卡住的更新器会被停止并给出明确消息，超时为 0 表示不限；以及窗口文本在八种语言中都存在。CI 运行 `python tools/ci_validate.py`（清单、版本、变更日志和 README 一致性），然后运行 `python tools/build_test.py`，它会编译每个源文件并运行测试。

## 🏗️ 构建与发布

版本号位于 `pyproject.toml`、`electro-hobby-3d.project.json` 和包中，每个版本在 [CHANGELOG.md](CHANGELOG.md) 中都有条目。`build.sh` / `build.bat` 创建虚拟环境，连同四个固定版本的更新器安装本工具并做编译检查；`build-test.sh` / `build-test.bat` 做同样的事然后运行测试；`test.sh` / `test.bat` 只运行测试，都在实时面板中进行，且都不会更改版本。版本发布在 GitHub 上（最新为 0.1.1）；该工具从本仓库安装，不在 PyPI 上。

## 🩺 故障排除

| 现象 | 处理办法 |
|---|---|
| 某个生态系统报告没有项目 | 更新器会在工作区中查找带有它清单的相邻文件夹；请用 `--workspace` 指定存放这些仓库的文件夹。 |
| `versions` 说某个更新器落后（退出码 2） | 固定版本是有意为之：审阅该更新器较新的提交，把它写入 `pyproject.toml`，提升本工具的版本并重新安装。 |
| 窗口打不开 | 需要 PySide6：`pip install -e ".[gui]"`；没有它命令行也能工作。 |
| 某个更新器运行时间太长 | 它在到达限制后被停止（`status` 900 秒，`install` 和 `update` 1800 秒）；用 `--timeout-seconds` 调高，或用 0 表示不限。 |
| ARMOR-UPDATER 在自我更新后损坏 | 它的可编辑安装指向其暂存文件夹：请手动更新 ARMOR-UPDATER，并再次运行 `build.bat` / `build.sh`。 |

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="ELECTRO-HOBBY-3D-UPDATER 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            唯一命名四个生态系统的地方
│   ├── main.py                                  命令行、分派和版本
│   ├── qt_gui.py qml/                           Qt Quick 窗口及其 QML
│   ├── i18n.py                                  八种语言的窗口文字
│   └── assets/                                  程序图标
├── tests/                                       针对模拟进程运行器的分派
├── docs/                                        架构图和结构图的数据
├── tools/                                       CI、构建、README 检查和绘图
├── images/                                      横幅图以及架构和仓库结构图片
├── .github/                                     CI 与发布工作流、Issue 和 PR 模板
├── build.sh build.bat                           在实时面板中创建虚拟环境、可编辑安装并检查
├── build-test.sh build-test.bat                 同样的步骤，然后运行真实的测试
├── run.sh run.bat                               启动窗口，带参数则为命令行
├── bump*.py                                     提升版本的脚本
├── electro-hobby-3d.project.json                清单：版本、角色和成熟度
├── pyproject.toml                               包及四个固定版本的更新器
├── CHANGELOG.md                                 每个版本的变更
├── SECURITY.md SUPPORT.md                       如何报告漏洞及在哪里提问
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   参与贡献、行为准则和许可证
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* `update` 尚未真实运行，`install` 只运行过一次；`status` 已对三个生态系统的真实检出运行过。
* 对 EH3D-UPDATER 的交接尚未通过本工具在真实检出上运行过。
* 按设计没有“跨所有生态系统更新全部”。
* 提交是否必须签名由各个更新器决定，而 A.R.M.O.R. 的更新器在更新自身时会破坏自己的安装。
* 该工具未经独立审查，也不在 PyPI 上。

**下一步**

* 通过本工具在真实检出上运行 EH3D 项目的 `status`、`install` 和 `update`。
* 随着四个更新器发布新版本，把固定版本移到经过审阅的较新提交。
* 在某个生态系统上真实运行一次 `update`，并记录出现的问题。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、汉语、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

本工具是 JuanenRac（Electro Hobby 3D）更新器家族的第五个成员；它包装另外四个，而不是取代其中任何一个：

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)：检测、安装和更新 HYDRA-UMC 仓库
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)：检测、安装和更新 URTC 仓库
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)：检测、安装和更新 A.R.M.O.R. 仓库
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)：检测、安装和更新 EH3D 仓库
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)、[URTC](https://github.com/JuanenRac/URTC)、[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) 和 [EH3D](https://github.com/JuanenRac/EH3D-DOCS)：四个生态系统本身

## 📚 文档

* [变更日志](CHANGELOG.md)：每个版本、改了什么、发现了什么。
* [贡献指南](CONTRIBUTING.md)、[安全政策](SECURITY.md)和[支持](SUPPORT.md)。
* 各生态系统自己的更新器的文档在它们各自的仓库中（见相关项目）。

## 🤝 参与贡献与社区

* 提交 pull request 之前请运行 `python -m pytest tests -q` 和 `python tools/ci_validate.py`，两者都必须通过。参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 有八种语言：修改文字时要同步修改全部八个文件，两张图片由 `tools/make_architecture.py` 和 `tools/make_structure.py` 根据 `docs/architecture.json` 和 `docs/structure.json` 绘制。
* 本工具必须保持为分派器：发现、安装或更新的逻辑属于该生态系统的更新器，而不属于这里；新增一个生态系统只需修改 `ecosystems.py` 中的一行。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later。见 [LICENSE](LICENSE)。套件的硬件设计使用 CERN OHL-S。
