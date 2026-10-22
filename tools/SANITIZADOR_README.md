# Sanitizador de publicação

O script `sanitizar_publicacao.py` foi criado para preparar uma cópia pública do RelatPy sem apagar conteúdo silenciosamente.

## Comportamento

- O modo padrão é somente simulação.
- Arquivos proibidos são movidos para uma pasta de quarentena fora do repositório.
- Arquivos alterados recebem backup fora do repositório.
- URLs, caminhos UNC, e-mails, IPs privados e possíveis segredos são substituídos apenas no trecho detectado.
- Termos próprios podem ser listados em `publication_terms.local.txt`.
- O script gera um relatório JSON das alterações.

## Termos personalizados

Crie na raiz do projeto:

```text
publication_terms.local.txt
```

Adicione um termo por linha, por exemplo:

```text
#&$&@&$&#@&
NOME_DO_RELATORIO_INTERNO
#&$&@&$&#@&
```

Esse arquivo deve permanecer no `.gitignore`.

## Simulação

```powershell
.\venv\Scripts\python.exe .\tools\sanitizar_publicacao.py
```

## Aplicação

```powershell
.\venv\Scripts\python.exe .\tools\sanitizar_publicacao.py --apply
```

Para confirmar sem prompt, apenas em automação controlada:

```powershell
.\venv\Scripts\python.exe .\tools\sanitizar_publicacao.py --apply --yes
```

## Revisão obrigatória

```powershell
git status --short
git diff
.\venv\Scripts\python.exe .\tools\auditar_publicacao.py
```

Se o código deixar de compilar, restaure o arquivo correspondente a partir da pasta de backup gerada pelo script. Não faça commit sem revisar as alterações.
