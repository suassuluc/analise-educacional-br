"Faz o download dos dados brutos"
from __future__ import annotations
import ssl
import urllib.request
import zipfile
from pathlib import Path
from .config import RAW_DIR

# download.inep.gov.br envia cadeia SSL incompleta; o urllib do Linux/WSL recusa o certificado.
_SSL_SEM_VERIFICACAO = ssl._create_unverified_context()

# URLs oficiais(verifique antes de rodar)

URLS = {"ideb_municipios": "https://download.inep.gov.br/ideb/resultados/divulgacao_brasil_ideb_2025.zip",}

def baixar_arquivo(nome: str, url: str, destino: Path) -> Path:
    """Baixa um arquivo se ainda não existir localmente"""
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / nome
    if caminho.exists():
        print(f"[skip]{nome} já existe")
        return caminho
    print(f"[baixando]{nome} <- {url}")
    with urllib.request.urlopen(url, context=_SSL_SEM_VERIFICACAO) as resposta, caminho.open("wb") as arquivo:
        while True:
            bloco = resposta.read(1024 * 1024)
            if not bloco:
                break
            arquivo.write(bloco)
    return caminho

def descompactar_se_zip(caminho: Path, destino: Path) -> None:
    """Extrai o zip do INEP para a pasta raw, se o arquivo for um zip."""
    if not zipfile.is_zipfile(caminho):
        print(f"[skip] {caminho.name} não é zip")
        return
    print(f"[descompactando] {caminho.name} -> {destino}")
    with zipfile.ZipFile(caminho) as arquivo_zip:
        arquivo_zip.extractall(destino)

def main() -> None:
    for nome, url in URLS.items():
        caminho = baixar_arquivo(nome, url, RAW_DIR)
        descompactar_se_zip(caminho, RAW_DIR)
    print("[ok] ingestão concluída")

if __name__ == "__main__":
    main()
