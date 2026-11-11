# Demonstração local do RelatPy

Objetivo aprovado: site fictício, seleção de período, três CSVs e downloads paralelos,
reaproveitando o executor existente, sem sistemas ou credenciais da empresa.

- [x] Criar testes para datas inválidas, filtragem e associação dos downloads.
- [ ] Implementar site loopback e entrada `python -m demo.run`.
- [ ] Validar os três downloads em Chromium e o status persistido do executor.
- [ ] Documentar clone limpo, dependências, limites, captura e execução no CI.
- [ ] Publicar a alteração em branch/PR e atualizar a referência no perfil.

Decisão: o demo tem entrada própria porque `main.py` e `downloader.py` dependem de
configuração operacional removida da amostra. Não restaurar esses dados.
Uma execução por processo, conforme o modelo global atual do executor.
