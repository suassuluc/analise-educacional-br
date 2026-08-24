"Faz o download dos dados brutos"
from __future__ import annotations
import urllib.request
from pathlib import Path
from .config import RAW_DIR

# URLs oficiais(verifique antes de rodar)

URLS = {"ideb_municipios": "https://download.inep.gov.br/dados_abertos/IDEB/2024/municipio_2024.zip",}

def baixar_arquivo(nome: str, url: str, destino: Path) -> Path:
    """Baixa um arquivo se ainda não existir localmente"""
    destino.parent.mkdir(parents=True, exist_ok=True)
    caminho = destino / nome
    if caminho.exists():
        print(f"[skip]{nome} já existe")
        return caminho
    print(f"[baixando]{nome} <- {url}")
    urllib.request.urlretrieve(url, caminho)
    return caminho

def main() -> None:
    for nome, url in URLS.items():
        baixar_arquivo(nome, url, RAW_DIR)
    print("[ok] ingestão concluída")

if __name__ == "__main__":
    main()