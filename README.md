# RelatPy — automação de relatórios web

**Estudo de automação em Python com interface local, worker independente e execução assíncrona.**

O RelatPy organiza tarefas de geração de relatórios: seleção de período, execução dos fluxos, acompanhamento de status, downloads e tratamento de falhas. O projeto explora problemas comuns de automação operacional, como esperas de interface e separação entre a janela de acompanhamento e o processo executor.

**Estado atual:** amostra pública sanitizada de arquitetura e implementação. Os módulos operacionais e a configuração privada foram retirados. Esta versão ainda precisa de um cenário fictício completo para ser executável de ponta a ponta por quem clonar o repositório.

## Stack

Python, asyncio, Playwright, Streamlit, Tkinter, subprocess, JSON, pathlib e scripts de inicialização Windows. Há preparação para empacotamento e distribuição local.

## Código disponível

- Interface Streamlit para parametrizar período e acompanhar execuções.
- Launcher e worker em processos separados.
- Orquestração assíncrona com limite de concorrência.
- Estados de execução e persistência de status em JSON.
- Rotinas de download, arquivos, cancelamento e diagnóstico.
- Ferramentas para revisar e sanitizar a publicação.

| Responsabilidade | Arquivo |
| --- | --- |
| Interface | [streamlit_app.py](ui/streamlit_app.py) |
| Execução independente | [worker.py](worker.py) |
| Concorrência e persistência de status | [executor.py](core/executor.py) |
| Orquestração de downloads | [downloader.py](downloader.py) |
| Controle da aplicação | [app_control.py](core/app_control.py) |
| Revisão de publicação | [auditar_publicacao.py](tools/auditar_publicacao.py) |

O executor usa arquivo temporário e substituição para atualizar o status, reduzindo o risco de leitores encontrarem um JSON parcialmente gravado. A execução em worker separado evita vincular todo o processamento à sessão visual do Streamlit.

## Limites da amostra pública

| Item | Situação |
| --- | --- |
| Seletores, URLs e fluxos privados | Intencionalmente não distribuídos |
| Configuração de relatórios | `downloader.py` depende de `config.RELATORIOS`, ausente na amostra |
| Entrada de execução manual | Contém substituição sanitizada que precisa ser corrigida antes de funcionar |
| Ambiente público de demonstração | Ainda não incluído |
| Testes de comportamento e CI | Próximas melhorias |

O erro da entrada manual envolve atribuir uma string sanitizada a duas variáveis por desempacotamento. A solução deverá fornecer um contrato de credenciais e um fluxo fictício; recolocar dados privados não é necessário.

A limitação pertence à versão distribuída. Não há comprovação pública de métricas de economia de tempo ou taxa de sucesso, portanto esses resultados não são afirmados aqui.

## Preparação do ambiente

Requer Windows 10/11, Python 3.12 recomendado e navegador compatível. Na raiz, em PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r Requisitos.txt
.\.venv\Scripts\python.exe -m pip check
```

O nome versionado é `Requisitos.txt`, com R maiúsculo.

A entrada de interface é `ui/streamlit_app.py`. O comando abaixo documenta o ponto de entrada, mas não supera a ausência da configuração e dos módulos privados:

```powershell
.\.venv\Scripts\python.exe -m streamlit run ui/streamlit_app.py
```

Para uma adaptação, implemente configuração e módulos próprios somente em páginas autorizadas. O próximo MVP público deve usar um site local fictício e gerar arquivos de exemplo sem exigir acesso corporativo.

## Validação disponível

```powershell
.\.venv\Scripts\python.exe tools/auditar_publicacao.py
```

A auditoria de publicação e a verificação de dependências não equivalem a testes funcionais de download, cancelamento ou recuperação.

Antes de publicar, revise também [o checklist](PUBLICATION_CHECKLIST.md). Não inclua credenciais, sessões, relatórios reais, endereços internos, logs operacionais ou capturas de aplicações privadas.

## Próximas entregas, em ordem

1. Criar configuração e automação de demonstração com página local fictícia.
2. Corrigir a entrada sanitizada e assegurar que um clone novo executa o exemplo.
3. Testar sucesso, falha, timeout, cancelamento e associação de download.
4. Adicionar CI com testes de comportamento e auditoria de publicação.
5. Revisar arquivos acidentais na raiz e padronizar formatação e nomes.
6. Registrar um vídeo curto e métricas do cenário fictício, com procedimento de medição.

## Escopo do portfólio

Este projeto serve como evidência de Python assíncrono, automação web, processos e manipulação de arquivos. A proposta do MVP público é permitir avaliar essas competências sem depender de uma organização ou ambiente interno.

[Resumo técnico de portfólio](README_PORTFOLIO.md) · [Auditoria e sanitização](tools/SANITIZADOR_README.md)
