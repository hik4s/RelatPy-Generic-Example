# RelatPy — resumo técnico de portfólio

O RelatPy explora automação de relatórios web com Python, asyncio e Playwright, acompanhada por uma interface local Streamlit. A versão pública é uma amostra sanitizada: não inclui configuração operacional nem os módulos privados.

Consulte o [README principal](README.md) para estado atual, preparação do ambiente, limitações e próximos passos. Este documento resume as decisões técnicas que podem ser avaliadas no código.

## Problema e solução proposta

Gerar relatórios manualmente envolve escolher períodos, aguardar processamento, identificar o download correto e organizar resultados. A proposta é separar a interface de acompanhamento da execução, parametrizar o período e registrar o estado de cada tarefa.

## Evidências presentes

| Decisão | Código | O que avaliar |
| --- | --- | --- |
| Worker separado da interface | [worker.py](worker.py), [interface](ui/streamlit_app.py) | Ciclo de vida e comunicação por estado |
| Orquestração assíncrona | [executor.py](core/executor.py) | Concorrência limitada e propagação de falhas |
| Persistência de status | [executor.py](core/executor.py) | Arquivo temporário e substituição |
| Organização dos resultados | [file_manager.py](core/file_manager.py) | Destinos, validação e tratamento de erros |
| Controle da execução | [app_control.py](core/app_control.py) | Identificação e encerramento do worker |
| Revisão de publicação | [auditoria](tools/auditar_publicacao.py) | Detecção de informações que não devem ser publicadas |

Esses arquivos demonstram escolhas de implementação. A confiabilidade do fluxo completo ainda precisa ser comprovada por testes e demonstração reproduzível na versão pública.

## O que a versão pública ainda não comprova

- Execução ponta a ponta a partir de um clone novo: falta a configuração de relatórios e um fluxo fictício.
- Funcionamento da entrada manual: há uma substituição sanitizada incompatível com o desempacotamento de credenciais.
- Recuperação, cancelamento e download sob falhas: precisam de testes automatizados.
- Economia de tempo, taxa de sucesso e uso em escala: não há medições públicas reproduzíveis.

Esperas por estado são preferíveis a pausas fixas, mas precisam de prazo e tratamento de falha. Exemplos com espera ilimitada não devem ser usados como prova de confiabilidade.

## Próxima demonstração proposta

Um site local fictício deve permitir selecionar período, simular processamento, gerar um CSV e provocar uma falha controlada. O roteiro deve mostrar sucesso, timeout e cancelamento sem depender de credenciais, URLs ou dados de uma organização.

Critério de aceite: uma pessoa consegue clonar, instalar e executar o exemplo seguindo o README, com testes e resultados observáveis.

## Competências relacionadas

Python assíncrono, automação web, processos, arquivos, interface local e diagnóstico. O histórico de uso e as contribuições pessoais devem ser descritos com fatos verificáveis, sem publicar material privado ou resultados não medidos.

[Checklist de publicação](PUBLICATION_CHECKLIST.md) · [Guia de sanitização](tools/SANITIZADOR_README.md)
