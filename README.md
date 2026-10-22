# RelatPy

Plataforma local de automação de relatórios web desenvolvida em Python. O projeto utiliza Playwright para navegação automatizada e Streamlit para acompanhamento das execuções em uma interface local.

> Esta é a versão pública e sanitizada do projeto. Fluxos específicos, seletores, endereços internos, nomes de sistemas, caminhos de rede, credenciais e arquivos gerados não fazem parte do repositório.

## Visão geral

O RelatPy automatiza tarefas repetitivas relacionadas à geração de relatórios em aplicações web autorizadas. A pessoa usuária seleciona um período e os fluxos desejados, inicia a execução e acompanha o andamento pelo painel.

O projeto foi criado para demonstrar uma solução completa de automação, incluindo preparação do ambiente, controle de processos, persistência de status, downloads, logs, cancelamento seguro e tratamento de falhas.

## Funcionalidades

- Interface local com Streamlit.
- Seleção de período inicial e final.
- Seleção individual ou conjunta de automações.
- Execução assíncrona com Playwright.
- Acompanhamento do status de cada fluxo.
- Download local dos arquivos gerados.
- Envio opcional para destinos previamente autorizados.
- Validação básica dos arquivos produzidos.
- Cancelamento seguro da execução.
- Limpeza controlada de arquivos temporários.
- Logs separados para interface e worker.
- Persistência local do estado da execução.
- Preparação e reparo do ambiente Python.
- Uso de navegador instalado no Windows.

## Arquitetura

```text
Launcher
   ↓
Preparação do ambiente
   ↓
Interface Streamlit
   ↓
Worker independente
   ↓
Orquestrador assíncrono
   ↓
Módulos privados de automação
   ↓
Downloads, validação e destino opcional
```

Estrutura pública recomendada:

```text
RelatPy/
├── launcher.py
├── worker.py
├── main.py
├── downloader.py
├── auth.py
├── requisitos.txt
├── .env.example
├── ui/
│   └── streamlit_app.py
├── core/
│   ├── app_control.py
│   └── executor.py
├── assets/
├── tools/
│   └── auditar_publicacao.py
├── README.md
├── README_PORTFOLIO.md
├── PUBLICATION_CHECKLIST.md
└── .gitignore
```

Os módulos específicos de relatório e as configurações operacionais permanecem fora do repositório público.

## Estados de execução

Cada automação pode assumir estados como:

- `PENDENTE`
- `EXECUTANDO`
- `CONCLUIDO`
- `ERRO`
- `REMOVIDO`
- `CANCELADO`

## Tecnologias

- Python 3.12
- asyncio
- Playwright
- Streamlit
- Tkinter
- python-dotenv
- PyInstaller
- JSON
- pathlib
- subprocess
- Git e GitHub
- PowerShell

## Requisitos para desenvolvimento

- Windows 10 ou Windows 11.
- Python 3.12 recomendado.
- Navegador Chromium compatível instalado.
- Acesso autorizado às aplicações que serão automatizadas.

## Preparação do ambiente

```powershell
py -3.12 -m venv .\venv
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\python.exe -m pip install --no-cache-dir -r .\requisitos.txt
```

Crie a configuração local a partir do exemplo:

```powershell
Copy-Item .\.env.example .\.env
```

O arquivo `.env` é local e nunca deve ser versionado.

## Execução em desenvolvimento

```powershell
.\venv\Scripts\python.exe -m streamlit run .\ui\streamlit_app.py
```

A interface é disponibilizada apenas no endereço local configurado pelo projeto.

## Testes básicos

Validar as dependências:

```powershell
.\venv\Scripts\python.exe -m pip check
```

Validar a sintaxe dos arquivos Python públicos:

```powershell
Get-ChildItem . -Recurse -Filter "*.py" |
    Where-Object {
        $_.FullName -notmatch "\SERVIDOR_EXEMPLO\CAMINHO_CENSURADO"
    } |
    ForEach-Object {
        .\venv\Scripts\python.exe -m py_compile $_.FullName
    }
```

Executar a auditoria de publicação:

```powershell
.\venv\Scripts\python.exe .\tools\auditar_publicacao.py
```

## Segurança e privacidade

A versão pública não deve conter:

- credenciais ou tokens;
- cookies ou estados de sessão;
- URLs internas;
- nomes de servidores;
- caminhos de compartilhamentos de rede;
- nomes de sistemas corporativos;
- nomes específicos de relatórios;
- módulos privados de automação;
- arquivos baixados;
- logs e evidências;
- screenshots de aplicações internas;
- bancos de dados locais;
- executáveis compilados com configurações internas;
- dados operacionais reais.

O projeto não desativa a validação TLS e não utiliza mecanismos para contornar controles de segurança.

## Limites da versão pública

A versão pública representa a arquitetura, a interface e os mecanismos genéricos de execução. Os fluxos concretos de navegação não são distribuídos porque podem conter seletores, regras de negócio e referências a ambientes privados.

Para adaptar o projeto a outro ambiente, implemente módulos próprios somente para aplicações em que exista autorização formal.

## Principais aprendizados

- Esperar condições reais da interface é mais confiável do que usar pausas fixas.
- Processos de automação devem permanecer separados da sessão visual.
- Downloads precisam ser associados à execução correta.
- Cancelamento deve abranger somente o worker atual e seus processos-filhos.
- Segredos e configurações operacionais não devem fazer parte do código público.
- Distribuição, observabilidade e recuperação de falhas são partes do produto.

## Publicação

Antes de enviar qualquer alteração:

```powershell
git status --short
.\venv\Scripts\python.exe .\tools\auditar_publicacao.py
git diff --cached
```

Consulte também o arquivo `PUBLICATION_CHECKLIST.md`.

## Licença e uso

Projeto demonstrativo de automação defensiva e autorizada. Cada pessoa ou organização é responsável por garantir autorização para automatizar aplicações e tratar os dados envolvidos.
