from pathlib import Path
import pandas as pd
import unicodedata
import re

# ---------------------------
# Configuração de caminhos
# ---------------------------
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Funções utilitárias
# ---------------------------
def clean_colname(col: str) -> str:
    """ Normaliza nomes de coluna para snake_case, sem acentos """
    nfkd = unicodedata.normalize("NFKD", str(col))
    no_accent = "".join([c for c in nfkd if not unicodedata.combining(c)])
    s = re.sub(r"\s+", "_", no_accent.lower().strip())
    return re.sub(r"[^a-z0-9_]", "", s)

def try_read_csv(path: Path):
    encodings = ["utf-8", "latin1", "cp1252"]
    for enc in encodings:
        for sep in [",",";"]:
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep, infer_datetime_format=True)
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
    raise ValueError(f"Não consegui ler {path}")

def inspect_and_save(key, filename):
    path = RAW_DIR / filename
    if not path.exists():
        print(f" Arquivo não encontrado: {path}")
        return None

    df = try_read_csv(path)
    df.columns = [clean_colname(c) for c in df.columns]

    print(f"\n📂 {filename}")
    print("Dimensões:", df.shape)
    print("Nulos:\n", df.isnull().sum())
    print("Tipos:\n", df.dtypes)
    print("Preview:\n", df.head())

    out_path = INTERIM_DIR / f"{key}_interim.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Salvou: {out_path}")
    return df

# ---------------------------
# Main
# ---------------------------
expected_files = {
    "agencias": "agencias.csv",
    "clientes": "clientes.csv",
    "colab_agencia": "colaborador_agencia.csv",
    "colaboradores": "colaboradores.csv",
    "contas": "contas.csv",
    "propostas": "propostas_credito.csv",
    "transacoes": "transacoes.csv"
}

def main():
    for key, filename in expected_files.items():
        inspect_and_save(key, filename)

if __name__ == "__main__":
    main()
