# Dados

## Fonte primária
- IDEB 2023 — municípios (Anos Finais do Ensino Fundamental)
- URL: https://download.inep.gov.br/...
- Data do download: 22-08-2026

## Como baixar
Execute:
    python -m src.ingestion

O script baixa e descompata automaticamente para `data/raw/ideb_2023_municipios.xlsx`.

## Aviso: verificação SSL desligada na ingestão

O site `download.inep.gov.br` envia a cadeia de certificados HTTPS incompleta. No WSL/Linux, o `urllib` do Python recusa o download (`CERTIFICATE_VERIFY_FAILED`). No navegador do Windows o mesmo link costuma abrir, porque Windows e WSL usam listas de certificados diferentes.

Por isso `src/ingestion.py` baixa **sem verificar o certificado SSL** (`ssl._create_unverified_context()`). Isso **não é a prática recomendada de segurança** — é um contorno local para o certificado do INEP.

Isso **não abre um buraco no sistema**: vale só neste script, nesta conexão. O restante do WSL e do Windows continua checando certificados.

O que se perde é a garantia de identidade **desse arquivo**. Em rede confiável o risco prático é baixo (dado público, URL fixa no código, sem senha). Em rede não confiável (Wi‑Fi público, DNS adulterado, proxy), alguém poderia entregar um zip falso.

Não copie este padrão para login, API com token ou instalação de pacotes.

### Prática recomendada

O correto é manter a **verificação SSL ligada**: o Python confere a cadeia de certificados e só baixa se o servidor for o INEP. O atalho atual existe porque o **servidor** manda a cadeia incompleta; a correção de verdade seria o INEP ajustar o certificado (ou o script passar a confiar de forma explícita no CA certo, ainda verificando).

Quando o certificado do site estiver ok, altere **dois pontos** em `src/ingestion.py`:

1. **Linhas 8–9** — hoje o contexto é criado sem verificação:

```python
# download.inep.gov.br envia cadeia SSL incompleta; o urllib do Linux/WSL recusa o certificado.
_SSL_SEM_VERIFICACAO = ssl._create_unverified_context()
```

Troque por um contexto padrão (verificação ligada):

```python
_SSL_CONTEXTO = ssl.create_default_context()
```

2. **Linha 23** — hoje o `urlopen` usa o contexto sem verificação:

```python
with urllib.request.urlopen(url, context=_SSL_SEM_VERIFICACAO) as resposta, caminho.open("wb") as arquivo:
```

Passe o contexto com verificação:

```python
with urllib.request.urlopen(url, context=_SSL_CONTEXTO) as resposta, caminho.open("wb") as arquivo:
```

Equivalente (e ainda mais simples): omitir o `context`. O `urlopen` volta a usar o SSL padrão do sistema, com verificação ligada.

Não reative a verificação “no escuro”: rode `python -m src.ingestion` depois da mudança. Se o INEP ainda estiver com a cadeia incompleta, o erro `CERTIFICATE_VERIFY_FAILED` volta. Nesse caso, mantenha o contorno documentado até o certificado ser corrigido.

## Licença
Dados públicos federais — livre uso conforme LAI (Lei 12.527/2011).