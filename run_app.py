import sys
import os
from streamlit.web import cli as stcli


def caminho_recurso(caminho_relativo):
    """Encontra o caminho correto dos arquivos, tanto rodando normalmente
    quanto rodando empacotado pelo PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, caminho_relativo)


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        caminho_recurso("app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())