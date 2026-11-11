# Demonstração local do RelatPy

Objetivo aprovado: site fictício, seleção de período, três CSVs e downloads paralelos,
reaproveitando o executor existente, sem sistemas ou credenciais da empresa.

- [x] Criar testes para datas inválidas, filtragem e associação dos downloads.
- [x] Implementar site loopback e entrada `python -m demo.run`.
- [x] Validar os três downloads em Chromium e o status persistido do executor.
- [x] Documentar clone limpo, dependências, limites, captura e execução no CI.
- [x] Publicar a alteração em branch/PR.

Validação em 11/11/2026: quatro testes passaram no Windows, inclusive em clone
independente; a CLI gerou os três CSVs e o status. Workflow Ubuntu `Public demo`
43022482037 concluído com sucesso. Revisão independente sem achados importantes.
A referência no perfil será atualizada após a integração da demonstração.

Decisão: o demo tem entrada própria porque `main.py` e `downloader.py` dependem de
configuração operacional removida da amostra. Não restaurar esses dados.
Uma execução por processo, conforme o modelo global atual do executor.
