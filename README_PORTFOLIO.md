# RelatPy: automação web com foco em confiabilidade

## Apresentação

O RelatPy é um projeto de portfólio desenvolvido em Python para automatizar a geração de relatórios em aplicações web autorizadas. A solução reúne interface local, navegação assíncrona, controle de processos, downloads, logs, cancelamento seguro e preparação automatizada do ambiente.

Esta documentação foi sanitizada para publicação. Nomes de aplicações internas, relatórios, servidores, seletores privados, caminhos de rede e dados operacionais foram removidos.

## Problema abordado

Processos de geração de relatórios costumam exigir várias ações repetitivas:

- acessar aplicações web;
- preencher filtros de período;
- selecionar parâmetros;
- aguardar o processamento;
- solicitar exportações;
- localizar o resultado correto;
- baixar e validar arquivos;
- organizar os resultados.

Além do tempo gasto, execuções manuais podem gerar arquivos duplicados, seleção incorreta de filtros e dificuldade para identificar a origem de uma falha.

## Solução

O RelatPy transforma o processo em uma aplicação local:

1. a pessoa usuária seleciona um período e os fluxos desejados;
2. a interface inicia um worker independente;
3. o worker autentica em um ambiente autorizado;
4. o Playwright executa os fluxos configurados;
5. os arquivos são baixados e validados;
6. o painel apresenta o estado de cada automação;
7. o envio para um destino autorizado pode ser habilitado ou desabilitado.

## Competências demonstradas

- Python assíncrono com `asyncio`.
- Automação web com Playwright.
- Interface local com Streamlit.
- Gerenciamento cuidadoso de processos no Windows.
- Persistência de estado em JSON.
- Manipulação segura de arquivos.
- Tratamento de erros e logs operacionais.
- Preparação automática de ambiente virtual.
- Empacotamento com PyInstaller.
- Versionamento com Git e GitHub.
- Segurança defensiva e proteção de dados.

## Arquitetura

```text
Entrada da aplicação
        ↓
Preparação e diagnóstico do ambiente
        ↓
Interface local
        ↓
Worker independente
        ↓
Orquestração assíncrona
        ↓
Módulos privados de automação
        ↓
Download e validação
        ↓
Destino local ou autorizado
```

### Interface

A interface permite:

- selecionar o período;
- selecionar automações;
- acompanhar estados;
- visualizar logs;
- baixar resultados;
- cancelar a execução;
- escolher se os arquivos serão enviados para um destino configurado.

### Worker

O worker executa a automação em processo separado. Essa decisão evita que uma atualização ou fechamento da aba interrompa imediatamente os fluxos em andamento.

O processo é identificado de forma específica, evitando comandos amplos que poderiam encerrar outras aplicações Python da máquina.

### Módulos de automação

Os fluxos concretos permanecem privados. Todos seguem um contrato comum semelhante a:

```python
return {
    "status": "CONCLUIDO",
    "arquivo": caminho_local,
}
```

A versão pública demonstra a arquitetura sem divulgar seletores, regras internas ou nomes de relatórios.

## Desafios técnicos

### Esperas baseadas em estado

Tempos fixos são frágeis: podem ser curtos em dias lentos e longos quando a página responde rapidamente. O projeto prioriza condições observáveis:

```python
await elemento.wait_for(
    state="visible",
    timeout=0,
)
```

Para downloads:

```python
async with page.expect_download(timeout=0) as download_info:
    await botao.click(timeout=0)
```

### Elementos visíveis, mas bloqueados

Algumas interfaces exibem elementos antes que estejam realmente interativos. Em vez de forçar cliques, o fluxo aguarda overlays e indicadores de carregamento desaparecerem.

### Associação do download correto

O sistema procura o resultado correspondente à execução atual, valida o estado de conclusão e somente então aciona o download.

### Persistência fora da sessão visual

O estado global não depende da sessão do navegador. Atualizar a página não deve apagar o andamento mantido pelo worker.

### Cancelamento seguro

O cancelamento valida o processo antes de encerrar a árvore correspondente, preserva resultados concluídos e evita afetar outros processos Python.

### Ambiente corporativo

O projeto utiliza o navegador já instalado no Windows, evitando práticas inseguras como desativar validações de certificado.

## Segurança aplicada

- Segredos fora do código-fonte.
- `.env` excluído do versionamento.
- API e painel limitados ao host local.
- Limpeza restrita a diretórios controlados.
- Validação do PID antes do encerramento.
- TLS preservado.
- Caminhos de saída não aceitos diretamente de entrada livre do usuário.
- Módulos e configurações privadas excluídos da versão pública.
- Auditoria automática antes da publicação.

## Como executar a versão de desenvolvimento

```powershell
py -3.12 -m venv .\venv
.\venv\Scripts\python.exe -m pip install -r .\requisitos.txt
.\venv\Scripts\python.exe -m streamlit run .\ui\streamlit_app.py
```

A execução real depende de módulos privados e de acesso autorizado às aplicações de origem.

## Como validar

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe .\tools\auditar_publicacao.py
```

## Melhorias futuras

- Receitas declarativas para reduzir código específico.
- Gravador guiado de novos fluxos.
- Evidências automáticas em falhas.
- Histórico persistente de execuções.
- Métricas de duração e confiabilidade.
- Testes com páginas simuladas.
- Pipeline automatizado de release.
- Assinatura digital do executável.

## Relevância profissional

O RelatPy demonstra capacidade de transformar uma necessidade operacional em um produto funcional. O desenvolvimento envolveu automação, interface, processos, arquivos, diagnóstico, segurança, empacotamento e documentação.

O projeto evidencia:

- decomposição de problemas;
- investigação de falhas;
- evolução incremental;
- preocupação com confiabilidade;
- proteção de dados;
- documentação técnica;
- uso prático de controle de versão.

## Observação de confidencialidade

A versão de portfólio não inclui nenhuma informação que identifique organizações, aplicações internas, relatórios operacionais, servidores ou compartilhamentos de rede. Exemplos são genéricos e não representam dados reais.
