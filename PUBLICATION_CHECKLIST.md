# Checklist de publicação segura

Use este checklist antes de transformar o RelatPy em repositório público ou compartilhar o projeto no LinkedIn.

## 1. Arquivos proibidos

- [ ] `.env` não está rastreado.
- [ ] Credenciais, tokens, cookies e estados de sessão não estão presentes.
- [ ] A pasta privada de relatórios não está presente.
- [ ] Não há arquivos CSV, Excel ou PDF reais.
- [ ] Não há logs, screenshots, HTML ou traces internos.
- [ ] Não há banco SQLite local.
- [ ] Não há executável compilado com configuração interna.
- [ ] Não há backup contendo versões antigas sensíveis.

## 2. Conteúdo proibido no código e documentação

- [ ] Nomes de organizações foram removidos.
- [ ] Nomes de aplicações internas foram removidos.
- [ ] Nomes específicos de relatórios foram removidos.
- [ ] URLs internas foram substituídas por exemplos.
- [ ] Servidores e caminhos UNC foram removidos.
- [ ] Usuários, e-mails e nomes de pessoas foram removidos.
- [ ] IDs, protocolos e números de ocorrência foram removidos.
- [ ] Seletores que revelem estrutura interna foram revisados.

## 3. Imagens

- [ ] Screenshots usam dados fictícios.
- [ ] Não há nomes, e-mails ou identificadores visíveis.
- [ ] Não há URL interna na barra do navegador.
- [ ] Não há caminho de rede ou nome de servidor.
- [ ] Metadados das imagens foram removidos quando necessário.

## 4. Git

Verifique os arquivos rastreados:

```powershell
git ls-files
```

Verifique arquivos ignorados:

```powershell
git status --ignored --short
```

Execute a auditoria:

```powershell
.\venv\Scripts\python.exe .\tools\auditar_publicacao.py
```

Revise o commit:

```powershell
git diff --cached
```

## 5. Arquivos já rastreados

O `.gitignore` não remove arquivos que já estão no histórico. Para retirar arquivos privados do índice sem apagá-los localmente:

```powershell
git rm -r --cached relatorios
```

Para outros arquivos:

```powershell
git rm --cached .env
git rm --cached config.py
```

Depois:

```powershell
git add .gitignore README.md README_PORTFOLIO.md PUBLICATION_CHECKLIST.md tools/auditar_publicacao.py
git status
git commit -m "docs: sanitiza projeto para portfólio público"
```

Se dados sensíveis já foram enviados ao GitHub, apenas removê-los em um novo commit não elimina o histórico. Nesse caso, revogue segredos expostos e reescreva o histórico com `git filter-repo` em uma cópia de segurança.

## 6. Aprovação

- [ ] A versão pública foi revisada separadamente da versão operacional.
- [ ] A organização autorizou a publicação quando aplicável.
- [ ] O repositório apresenta apenas arquitetura e exemplos genéricos.
