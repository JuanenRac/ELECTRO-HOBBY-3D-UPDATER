<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center">
  <a href="README.md">🇺🇸 English</a> |
  <a href="README_spa.md">🇪🇸 Español</a> |
  <a href="README_fra.md">🇫🇷 Français</a> |
  <a href="README_ita.md">🇮🇹 Italiano</a> |
  <a href="README_deu.md">🇩🇪 Deutsch</a> |
  <a href="README_zho.md">🇨🇳 简体中文</a> |
  <a href="README_jpn.md">🇯🇵 日本語</a> |
  <b>🇵🇹 Português</b>
</p>

### Uma só linha de comandos para os três ecossistemas Electro Hobby 3D - escolha um sistema, descarregue e atualize os respetivos pacotes

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0-blue.svg" alt="GPL 3.0">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-3776ab.svg" alt="Language">
  <img src="https://img.shields.io/badge/Dependencies-3%20real%20sub--updaters-2ea44f.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Tests-13-00E5FF.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-functional-4caf50.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** **Maturidade: funcional.** Isto é um despachante fino, não uma quarta implementação da deteção de ecossistemas: não tem lógica própria de leitura de manifestos, de instalação nem de atualização. `dispatch()` e a construção dos seus comandos (16 testes, todos contra um executor de subprocessos simulado) são reais e estão testados; `status --ecosystem all` foi executado a sério contra uma cópia real dos três ecossistemas (55 repositórios HYDRA-UMC + 7 URTC + 17 A.R.M.O.R. encontrados corretamente) - O `install` também foi executado a sério, a partir de um ambiente limpo, e o ARMOR-COMMON foi clonado, compilado, testado e promovido pelo atualizador do ARMOR (as revisões sem assinatura são instaladas com um aviso); o `update` ainda não foi executado a sério. Foi encontrado e corrigido um erro real durante essa primeira execução real: ver a entrada `--workspace` do `CHANGELOG.md`.

---

## 🎯 Visão geral

* **Uma só ferramenta, três ecossistemas reais:** o [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), o [URTC](https://github.com/JuanenRac/URTC-UPDATER) e o [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) já têm cada um o seu atualizador dedicado e testado de forma independente. Este projeto não reimplementa nada disso - instala os três como dependências reais e despacha `--ecosystem hydra-umc|urtc|armor` para o que corresponde.
* **Dependências fixadas e revistas:** o `pyproject.toml` fixa cada sub-atualizador num commit revisto, nunca num `main` em movimento, pelo que uma instalação obtém sempre exatamente o que foi revisto. `versions` mostra a versão instalada de cada um e assinala os que estão atrasados em relação ao GitHub.
* **Um subprocesso real e separado de cada vez.** Cada chamada executa `python -m <módulo do ecossistema> --cli ...` como um processo de interpretador próprio - nunca importa o `main()` da CLI de outro para este. Três programas argparse independentes, cada um livre de analisar `sys.argv` e de chamar `sys.exit()`, corromper-se-iam uns aos outros se fossem compostos no mesmo processo.
* **`status --ecosystem all`:** executa em simultâneo as verificações de estado dos três ecossistemas, imprime cada relatório completo numa ordem fixa e indica quais falharam sem parar à primeira falha.
* **`install`/`update` precisam sempre de um ecossistema e de um nome de projeto.** Não existe aqui um "atualizar tudo em todos os ecossistemas", a mesma posição que a CLI de cada sub-atualizador já adota.
* **Limites herdados:** esta ferramenta executa o que cada sub-atualizador faz. O atualizador do A.R.M.O.R. continua a danificar a sua própria instalação quando se atualiza a si mesmo (a instalação editável aponta para o seu diretório de preparação), por isso atualize o ARMOR-UPDATER à mão por agora. O URTC-UPDATER pode exigir commits assinados (`URTC_UPDATER_REQUIRE_SIGNED=1`); os outros dois ainda não verificam assinaturas.

## 📂 Estrutura do repositório

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py   # The one place naming the three real ecosystems and their CLI module
│   ├── main.py         # argparse CLI + dispatch() - builds and runs the right subprocess command
│   ├── i18n.py         # The words of the window in the eight languages
│   ├── qt_gui.py       # Qt Quick window (a card per ecosystem, a log) - opens each ecosystem's own updater
│   └── qml/Main.qml    # The window's QML
├── tests/               # 16 tests against a fake subprocess runner
├── tools/               # ci_validate.py, build_test.py, _doc_policy.py, _readme_parity.py
├── build.sh / build.bat         # venv + editable install (pulls the 3 real dependencies) + compile-check
├── build-test.sh / build-test.bat  # same install, then the real pytest suite
└── run.sh / run.bat              # CLI entry point (no arguments: the window)
```

## 🛠️ Ambiente de desenvolvimento

```bash
pip install -e ".[dev]"                 # also installs hydra-umc-updater, urtc-updater, armor-updater from GitHub
python -m pytest tests -q               # 16 tests, no network or real subprocess needed
electro-hobby-3d-updater status --ecosystem all               # check every ecosystem (in parallel)
electro-hobby-3d-updater versions                             # installed version of each updater, and whether it is behind GitHub
electro-hobby-3d-updater status --ecosystem armor             # check just one
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER # clone + build one project not yet installed
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER # pull + rebuild one project already installed
```

## 🔗 Projetos relacionados

Esta ferramenta é a quarta peça da família de atualizadores própria de JuanenRac (Electro Hobby 3D) - envolve as outras três em vez de substituir qualquer uma delas:

* **[HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER)** - deteta, instala e atualiza os repositórios do próprio ecossistema HYDRA-UMC
* **[URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)** - deteta, instala e atualiza os repositórios do próprio ecossistema URTC
* **[ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER)** - deteta, instala e atualiza os repositórios do próprio ecossistema A.R.M.O.R.
* **ELECTRO-HOBBY-3D-UPDATER** (este repositório) - despacha para aquele dos três que o utilizador escolher

E os próprios três ecossistemas reais: **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** (controlo industrial de células multirrobô), **[URTC](https://github.com/JuanenRac/URTC)** (a plataforma Universal Robot Tool Controller), **[A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON)** (segurança perimetral e domótica).

## 📚 Documentação e comunidade

* **[Registo de alterações deste repositório](CHANGELOG.md)**
* Perguntas, ideias e relatórios: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

GPL-3.0-or-later - ver [LICENSE](LICENSE).
