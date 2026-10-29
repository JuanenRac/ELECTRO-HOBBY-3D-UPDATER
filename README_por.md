<p align="center">
  <img src="images/ELECTRO_HOBBY_3D_BANNER.svg" alt="ELECTRO-HOBBY-3D-UPDATER banner" width="100%">
</p>

# 🧩 ELECTRO-HOBBY-3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### Uma linha de comandos e uma janela para os quatro ecossistemas da Electro Hobby 3D: escolhe um sistema, descarrega e atualiza os seus pacotes com o atualizador que esse sistema já tem

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-functional-4CAF50.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** isto é um despachante fino, não uma quinta implementação da descoberta de ecossistemas: não tem lógica própria de análise de manifestos, instalação ou atualização. Cada um dos quatro ecossistemas tem o seu próprio atualizador, que encontra os seus projetos pelo manifesto `<ecossistema>.project.json` de cada repositório; esta ferramenta instala os quatro como dependências fixadas e executa o que escolhes como um processo à parte (`status` para os quatro ao mesmo tempo). O despacho e os comandos que constrói estão testados (passam 18 testes, com um executor de processos simulado). `status --ecosystem all` foi executado a sério contra uma cópia real de três dos ecossistemas e `install` uma vez a partir de um ambiente limpo (um projeto clonado, construído, testado e promovido pelo atualizador do A.R.M.O.R.); `update` não foi executado a sério, e a passagem ao atualizador do EH3D foi acrescentada a partir dos testes desse atualizador e não foi executada por esta ferramenta contra uma cópia real.

---

> **Estado de segurança (safety) e de segurança informática:** substitui ficheiros na tua máquina através dos atualizadores que executa, por isso só faz o que cada um deles faz, um projeto de cada vez e após a confirmação que esse atualizador pede. Não executa nada sozinho, nunca atualiza «tudo através dos ecossistemas» e não controla nenhuma máquina. Cada atualizador está fixado a um commit revisto, nunca a um ramo que se move; as revisões sem assinatura são instaladas com um aviso, a menos que esse atualizador esteja configurado para exigir assinaturas.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.1.1` |
| Maturidade | Funcional |
| Testes | 18 |
| Tecnologias | Python 3.10+ (PySide6 for the window) |
| Em hardware real | Não se aplica: corre no PC da pessoa que o usa |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Software | 🟡 | Um despachante fino: não tem lógica própria de descoberta, instalação ou atualização e passa `--ecosystem hydra-umc\|urtc\|armor\|eh3d` ao atualizador de cada ecossistema, que instala como dependências fixadas. |
| Testes | 🟢 | Passam 18 testes (`pytest`) contra um executor de processos simulado; outro é ignorado quando o PySide6 não está instalado. |
| Uso real | 🟠 | `status` foi executado contra uma cópia real de três dos ecossistemas e `install` uma vez a partir de um ambiente limpo; `update` não foi executado a sério. |
| Janela | 🟡 | A janela (um cartão por ecossistema, um registo, oito idiomas) abre o atualizador próprio de cada ecossistema; os seus textos e as suas regras de threads estão testados, o resto só à mão. |
| Integração | 🟠 | A passagem ao atualizador do EH3D foi acrescentada a partir dos testes desse atualizador e não foi executada por este despachante contra uma cópia real. |
| Segurança | 🟡 | Cada sub-atualizador está fixado a um commit revisto, nunca a um ramo que se move; cada execução é um processo à parte com limite de tempo; as revisões sem assinatura são instaladas com um aviso e não houve revisão independente. |
| Hardware real | 🟢 | Não se aplica: corre no PC da pessoa que o usa. |
| Documentação | 🟢 | README em oito idiomas, verificado em cada alteração contra o manifesto e o registo de alterações. |

## 🎯 Visão geral

* **Uma ferramenta, quatro ecossistemas:** [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC-UPDATER), [URTC](https://github.com/JuanenRac/URTC-UPDATER), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-UPDATER) e [EH3D](https://github.com/JuanenRac/EH3D-UPDATER) têm cada um o seu atualizador, testado em separado. Este projeto não reimplementa nada disso: instala os quatro como dependências e passa `--ecosystem hydra-umc|urtc|armor|eh3d` ao que corresponde.
* **A descoberta fica em cada atualizador:** cada ecossistema encontra os seus projetos pelo manifesto de cada repositório (`hydra-umc.project.json`, `urtc.project.json`, `armor.project.json`, `eh3d.project.json`), por isso um repositório novo aparece no seu ecossistema por ter um manifesto e nada nesta ferramenta enumera os projetos. O manifesto desta ferramenta, `electro-hobby-3d.project.json`, não pertence a nenhum dos quatro por desenho.
* **Dependências fixadas e revistas:** `pyproject.toml` fixa cada atualizador a um commit revisto, nunca a um `main` que se move. `versions` mostra a versão instalada de cada um e assinala os que estão atrás do GitHub.
* **Um processo à parte de cada vez:** cada chamada executa `python -m <módulo desse ecossistema> --cli ...` como o seu próprio interpretador; quatro programas argparse que podem chamar `sys.exit()` estragar-se-iam uns aos outros num só processo.
* **`status --ecosystem all`:** executa as quatro verificações de estado ao mesmo tempo, imprime cada relatório inteiro numa ordem fixa e diz quais falharam sem parar no primeiro.
* **`install` e `update` precisam sempre de um ecossistema e de um nome de projeto:** não há «atualizar tudo em todos os ecossistemas», a mesma posição de cada atualizador.
* **Uma janela:** sem argumentos, uma janela Qt Quick mostra um cartão por ecossistema e um registo, abre o atualizador próprio de cada ecossistema e pede-lhe o seu estado, em oito idiomas.

## 🧩 Papel no Electro Hobby 3D

O ELECTRO-HOBBY-3D-UPDATER é a quinta peça da família de atualizadores da Electro Hobby 3D e está acima dos quatro ecossistemas: envolve os outros quatro em vez de substituir algum. É o único sítio onde quem trabalha com mais de um ecossistema pode ver todos e escolher qual atualizar.

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura de ELECTRO-HOBBY-3D-UPDATER: quem o usa, o que contém e de que depende" width="100%">
</p>

Como as partes deste repositório se encaixam: quem o usa, o que contém e de que depende. A imagem é desenhada a partir de `docs/architecture.json` e verificada com o código.

## 🔒 Segurança e proteção

| Ameaça | Defesa |
|---|---|
| Um `main` móvel ou comprometido de um atualizador a chegar a esta ferramenta | cada atualizador está fixado em `pyproject.toml` a um commit revisto, nunca a um ramo; para passar a um mais recente revê-se primeiro e muda-se aqui a fixação |
| Um atualizador a estragar outro | cada chamada executa o atualizador como o seu próprio processo de interpretador (`python -m <módulo> --cli ...`), nunca importado neste, por isso nenhum pode mudar os argumentos, o estado ou a saída de outro |
| Um atualizador que bloqueia (um pedido de credenciais do git, uma rede morta) | um limite de tempo em cada execução: 900 s para `status` e 1800 s para `install` e `update`, alterável com `--timeout-seconds` (0 significa sem limite) |
| Uma alteração em massa indesejada | `install` e `update` recebem exatamente um ecossistema e um nome de projeto e recusam `--ecosystem all`; cada atualizador pede a sua própria confirmação |
| Olhar para a pasta errada | a área de trabalho é sempre reenviada de forma explícita (por omissão a pasta-mãe desta ferramenta), porque de outro modo um atualizador instalado procuraria no ambiente virtual desta e não encontraria nada em silêncio |
| Um commit de origem desconhecida | fica a cargo de cada atualizador: as revisões sem assinatura são instaladas com um aviso a menos que se diga a esse atualizador para exigir assinaturas (o EH3D-UPDATER e o URTC-UPDATER têm essa opção) |
| A falha de um ecossistema a esconder os outros | `status --ecosystem all` executa os quatro, imprime cada relatório e nomeia os que falharam |

**O que não é defendido:** esta ferramenta executa o que cada atualizador faz, com os teus direitos, incluindo o script de compilação do projeto que instalas; o atualizador do A.R.M.O.R. ainda estraga a sua própria instalação quando se atualiza a si mesmo, por isso atualiza o ARMOR-UPDATER à mão; e a ferramenta não teve revisão independente. Comunica uma vulnerabilidade em privado (ver [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | O que é | Onde |
|---|---|---|
| Linha de comandos | `electro-hobby-3d-updater` com `status`, `install`, `update` e `versions`; `--version`; códigos de saída 0, 1 (uma execução falhou ou esgotou o tempo) e 2 (`versions`: um atualizador está atrás do GitHub) | `main.py` |
| Janela | sem argumentos abre uma janela Qt Quick (um cartão por ecossistema e um registo); precisa do extra opcional `PySide6` | `qt_gui.py`, `qml/Main.qml` |
| Para cada atualizador | um processo à parte: `python -m <hydra_umc_updater.main, urtc_updater.main, armor_updater.main ou eh3d_updater.main> --cli <ação> [projeto] --workspace <pasta>` | `ecosystems.py` |
| GitHub | `versions` lê o `pyproject.toml` do repositório de cada atualizador em `main` para comparar versões; nada mais | `main.py` |

## ⚙️ Configuração

Não é preciso configurar nada; as opções da linha de comandos são toda a configuração, e tudo o resto pertence a cada atualizador.

| Opção | Por omissão | Gama | O que faz |
|---|---|---|---|
| `--ecosystem` | nenhum | `hydra-umc`, `urtc`, `armor` ou `eh3d`; `all` só para `status` | que atualizador faz o trabalho |
| `--workspace` | a pasta-mãe desta ferramenta | uma pasta | a área de trabalho que cada atualizador percorre (sempre reenviada) |
| `--offline` (`status`, `versions`) | desativado | ativado ou desativado | saltar a verificação do GitHub |
| `--timeout-seconds` | 900 para `status`, 1800 para `install` e `update` | um número de segundos; 0 ou menos significa sem limite | parar um atualizador que não terminou |
| as fixações | quatro commits em `pyproject.toml` | um commit revisto de cada atualizador | que código de atualizador se instala; só muda depois de rever um mais recente |

As fixações desta versão são HYDRA-UMC-UPDATER 0.4.8, URTC-UPDATER 0.1.7, ARMOR-UPDATER 0.1.4 e EH3D-UPDATER 0.0.1.

## 🚀 Início rápido

Precisa de Python 3.10 ou mais recente; a janela precisa também do PySide6.

```bash
build.bat                                   # ./build.sh on Linux: a venv and an editable install (pulls the four pinned updaters)
pip install -e ".[dev]"                     # the same by hand; add ".[gui]" for the window
python -m pytest tests -q
electro-hobby-3d-updater status --ecosystem all
electro-hobby-3d-updater versions
electro-hobby-3d-updater install --ecosystem urtc URTC-TESTER
electro-hobby-3d-updater update  --ecosystem hydra-umc HYDRA-UMC-SERVER
```

`run.bat` / `run.sh` sem argumentos abrem a janela. `install` e `update` precisam de um ecossistema e de um nome de projeto, escrito como o manifesto desse ecossistema o declara.

## 🧪 Testes

A suite tem 18 testes que passam (`pytest tests`), e mais um que é ignorado quando o PySide6 não está instalado. Correm contra um executor de processos simulado, sem rede nem subprocessos reais, e cobrem: o registo tem exatamente os quatro ecossistemas; `status` executa o módulo certo e reenvia `--offline`; `status --ecosystem all` executa cada ecossistema uma vez, imprime-os por ordem, executa-os ao mesmo tempo e nunca pára na primeira falha; `install` e `update` precisam de um ecossistema e de um projeto e recusam `all`; um atualizador que falha passa o seu próprio código de saída; a área de trabalho é por omissão a pasta-mãe; `versions` informa as versões instaladas, assinala um atualizador atrasado e nunca contacta o GitHub com `--offline`; um atualizador que bloqueia é parado com uma mensagem clara e um limite de tempo de zero significa sem limite; e os textos da janela existem nos oito idiomas. A CI executa `python tools/ci_validate.py` (manifesto, versão, registo de alterações e paridade dos README) e depois `python tools/build_test.py`, que compila cada fonte e executa a suite.

## 🏗️ Compilação e publicação

A versão vive em `pyproject.toml`, em `electro-hobby-3d.project.json` e no pacote, e cada versão tem a sua entrada em [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` criam um ambiente virtual, instalam esta ferramenta com os seus quatro atualizadores fixados e verificam-na por compilação; `build-test.sh` / `build-test.bat` fazem o mesmo e depois executam a suite; `test.sh` / `test.bat` executam só os testes, cada um num painel em direto, e nenhum altera a versão. As versões são publicadas no GitHub (a mais recente é a 0.1.1); a ferramenta instala-se a partir deste repositório e não está no PyPI.

## 🩺 Resolução de problemas

| Sintoma | O que fazer |
|---|---|
| Um ecossistema não indica projetos | O atualizador procura na área de trabalho pastas vizinhas com o seu manifesto; passa `--workspace` com a pasta que contém os repositórios. |
| `versions` diz que um atualizador está ATRÁS (código de saída 2) | As fixações são deliberadas: revê o commit mais recente desse atualizador, põe-no em `pyproject.toml`, sobe a versão desta ferramenta e reinstala. |
| A janela não abre | Precisa do PySide6: `pip install -e ".[gui]"`; a linha de comandos funciona sem ele. |
| Um atualizador demorou demasiado | Foi parado ao atingir o limite (900 s para `status`, 1800 s para `install` e `update`); sobe-o com `--timeout-seconds`, ou 0 para não ter limite. |
| O ARMOR-UPDATER estraga-se depois de se atualizar a si mesmo | A sua instalação editável aponta para a sua pasta de preparação: atualiza o ARMOR-UPDATER à mão e executa de novo `build.bat` / `build.sh`. |

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório ELECTRO-HOBBY-3D-UPDATER" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
ELECTRO-HOBBY-3D-UPDATER/
├── src/electro_hobby_3d_updater/
│   ├── ecosystems.py                            o único sítio que nomeia os quatro ecossistemas
│   ├── main.py                                  a linha de comandos, o despacho e as versões
│   ├── qt_gui.py qml/                           a janela Qt Quick e o seu QML
│   ├── i18n.py                                  as palavras da janela em oito idiomas
│   └── assets/                                  o ícone do programa
├── tests/                                       o despacho contra um executor de processos simulado
├── docs/                                        os dados das imagens de Arquitetura e Estrutura
├── tools/                                       CI, construção, README e imagens
├── images/                                      banner e as imagens de Arquitetura e Estrutura do repositório
├── .github/                                     fluxos de CI e de publicação, modelos de issues e pull requests
├── build.sh build.bat                           venv, instalação editável e verificação num painel em direto
├── build-test.sh build-test.bat                 o mesmo, e depois a suite de testes real
├── run.sh run.bat                               abre a janela, ou a linha de comandos com argumentos
├── bump*.py                                     os scripts que sobem a versão
├── electro-hobby-3d.project.json                o manifesto: versão, papel e maturidade
├── pyproject.toml                               o pacote e os quatro atualizadores fixados
├── CHANGELOG.md                                 o que mudou em cada versão
├── SECURITY.md SUPPORT.md                       como comunicar uma vulnerabilidade e onde perguntar
└── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   como contribuir, o código de conduta e a licença
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* `update` não foi executado a sério, e `install` só uma vez; `status` foi executado contra uma cópia real de três ecossistemas.
* A passagem ao EH3D-UPDATER não foi executada por esta ferramenta contra uma cópia real.
* Não há «atualizar tudo em todos os ecossistemas», por desenho.
* Saber se um commit tem de estar assinado fica a cargo de cada atualizador, e o atualizador do A.R.M.O.R. estraga a sua própria instalação quando se atualiza a si mesmo.
* A ferramenta não teve revisão independente e não está no PyPI.

**A seguir**

* Executar `status`, `install` e `update` dos projetos EH3D por esta ferramenta numa cópia real.
* Mover as fixações para commits revistos mais recentes dos quatro atualizadores à medida que publiquem.
* Executar `update` a sério num ecossistema e registar o que aparecer.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

Esta ferramenta é a quinta peça da família de atualizadores de JuanenRac (Electro Hobby 3D); envolve os outros quatro em vez de substituir algum:

* [HYDRA-UMC-UPDATER](https://github.com/JuanenRac/HYDRA-UMC-UPDATER): deteta, instala e atualiza os repositórios do HYDRA-UMC
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): deteta, instala e atualiza os repositórios do URTC
* [ARMOR-UPDATER](https://github.com/JuanenRac/ARMOR-UPDATER): deteta, instala e atualiza os repositórios do A.R.M.O.R.
* [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER): deteta, instala e atualiza os repositórios do EH3D
* [HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC), [URTC](https://github.com/JuanenRac/URTC), [A.R.M.O.R.](https://github.com/JuanenRac/ARMOR-COMMON) e [EH3D](https://github.com/JuanenRac/EH3D-DOCS): os quatro ecossistemas em si

## 📚 Documentação

* [Registo de alterações](CHANGELOG.md): cada versão, o que mudou e o que foi encontrado.
* [Contribuir](CONTRIBUTING.md), [Política de segurança](SECURITY.md) e [Suporte](SUPPORT.md).
* A documentação do atualizador próprio de cada ecossistema vive no seu repositório (ver Projetos relacionados).

## 🤝 Contribuir e comunidade

* Antes de um pull request execute `python -m pytest tests -q` e `python tools/ci_validate.py`: ambos têm de passar. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito idiomas: uma alteração ao texto faz-se nos oito ficheiros, e as duas imagens são desenhadas a partir de `docs/architecture.json` e `docs/structure.json` com `tools/make_architecture.py` e `tools/make_structure.py`.
* Esta ferramenta tem de continuar a ser um despachante: a lógica que descobre, instala ou atualiza pertence ao atualizador do ecossistema, não a esta, e um ecossistema novo é uma alteração de uma linha em `ecosystems.py`.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later. Ver [LICENSE](LICENSE). Os projetos de hardware da suite usam a CERN OHL-S.
