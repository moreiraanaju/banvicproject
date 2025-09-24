# ============================================================
# 02_clean_transform.py
# Objetivo:
#  - Carregar dados intermediários (data/interim/)
#  - Tratar colunas (datas, numéricos, strings)
#  - Criar colunas derivadas (sazonalidade, fim de semana etc.)
#  - Validar consistência e qualidade dos dados
#  - Salvar versões limpas em data/processed/
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np


# ------------------------------
# Configurações
# ------------------------------
DATA_INTERIM = Path("data/interim")
DATA_PROCESSED = Path("data/processed")
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# ------------------------------
# Funções auxiliares
# ------------------------------
def load_csv(path):
    """Carrega CSV com tratamento básico de encoding e separador"""
    return pd.read_csv(path, encoding="utf-8", sep=",")

def print_quality_report(df, name):
    """Exibe relatório de qualidade do DataFrame"""
    print(f"\n{'='*80}")
    print(f"📊 INSPEÇÃO DO DATAFRAME: {name}")
    print(f"{'='*80}")
    print("\n👉 Head:")
    print(df.head())

    print("\n👉 Info:")
    print(df.info())

    print("\n👉 Valores nulos por coluna:")
    print(df.isna().sum())

    print("\n👉 Duplicatas:", df.duplicated().sum())

    print("\n👉 Estatísticas descritivas:")
    print(df.describe(include="all").transpose())

# Função para calcular estação do ano
def get_season(date):
    if pd.isnull(date):
        return np.nan
    m = date.month
    d = date.day
    if (m == 12 and d >= 21) or (1 <= m <= 2) or (m == 3 and d < 21):
        return "Verão"
    elif (m == 3 and d >= 21) or (4 <= m <= 5) or (m == 6 and d < 21):
        return "Outono"
    elif (m == 6 and d >= 21) or (7 <= m <= 8) or (m == 9 and d < 23):
        return "Inverno"
    else:
        return "Primavera"

# ------------------------------
# Carregar bases
# ------------------------------
print("\n🚀 Carregando bases intermediárias...")

agencias = load_csv(DATA_INTERIM / "agencias_interim.csv")
clientes = load_csv(DATA_INTERIM / "clientes_interim.csv")
colab_agencia = load_csv(DATA_INTERIM / "colab_agencia_interim.csv")
colaboradores = load_csv(DATA_INTERIM / "colaboradores_interim.csv")
contas = load_csv(DATA_INTERIM / "contas_interim.csv")
propostas = load_csv(DATA_INTERIM / "propostas_interim.csv")
transacoes = load_csv(DATA_INTERIM / "transacoes_interim.csv")

# ------------------------------
# Tratamento de datas
# ------------------------------
print("\n🛠️ Convertendo colunas de datas de forma robusta...")

# Dicionário de colunas que devem ser convertidas para datetime
date_cols = {
    "agencias": ["data_abertura"],
    "clientes": ["data_inclusao", "data_nascimento"],
    "contas": ["data_abertura", "data_ultimo_lancamento"],
    "propostas": ["data_entrada_proposta"],
    "transacoes": ["data_transacao"]
}

# Loop geral para todas as tabelas
for df_name, cols in date_cols.items():
    df = locals()[df_name]  # pega o dataframe pelo nome
    for col in cols:
        # 1) Converter para string e limpar UTC + microsegundos
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r'(\.\d+)?\s?UTC$', '', regex=True)
        )
        # 2) Converter para datetime sem timezone
        df[col] = pd.to_datetime(df[col], errors="coerce")

        # Exibir quantidade de nulos
        print(f"{df_name}.{col} → Nulos: {df[col].isna().sum()}")

        # Se houver nulos, mostrar exemplos
        if df[col].isna().sum() > 0:
            print(f"   Exemplos inválidos em {df_name}.{col}:")
            print(df.loc[df[col].isna(), col].head(5))


# ------------------------------
# Tratamento de numéricos
# ------------------------------
print("\n🛠️ Convertendo colunas numéricas...")

numeric_cols = {
    "contas": ["saldo_total", "saldo_disponivel"],
    "propostas": ["taxa_juros_mensal", "valor_proposta", "valor_financiamento",
                  "valor_entrada", "valor_prestacao"],
    "transacoes": ["valor_transacao"]
}

for df_name, cols in numeric_cols.items():
    df = locals()[df_name]
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ------------------------------
# Criar colunas derivadas em transações
# ------------------------------
print("\n✨ Criando colunas derivadas em transações...")

transacoes["day_name"] = transacoes["data_transacao"].dt.day_name(locale="pt_BR")
transacoes["is_weekend"] = transacoes["data_transacao"].dt.weekday >= 5
transacoes["is_month_even"] = transacoes["data_transacao"].dt.month % 2 == 0
transacoes["season"] = transacoes["data_transacao"].apply(get_season)

# ------------------------------
# Criar colunas derivadas em propostas
# ------------------------------
print("\n✨ Criando colunas derivadas em propostas...")

propostas["year_month"] = propostas["data_entrada_proposta"].dt.to_period("M")
propostas["ticket_medio"] = propostas["valor_proposta"] / propostas["quantidade_parcelas"].replace(0, np.nan)

# ------------------------------
# Relatórios de qualidade
# ------------------------------
print_quality_report(transacoes, "TRANSACOES (após transformações)")
print_quality_report(propostas, "PROPOSTAS (após transformações)")
print_quality_report(contas, "CONTAS")
print_quality_report(clientes, "CLIENTES")

# ------------------------------
# Salvar versões processadas
# ------------------------------
print("\n💾 Salvando versões processadas em data/processed/...")

agencias.to_csv(DATA_PROCESSED / "agencias.csv", index=False)
clientes.to_csv(DATA_PROCESSED / "clientes.csv", index=False)
colab_agencia.to_csv(DATA_PROCESSED / "colab_agencia.csv", index=False)
colaboradores.to_csv(DATA_PROCESSED / "colaboradores.csv", index=False)
contas.to_csv(DATA_PROCESSED / "contas.csv", index=False)
propostas.to_csv(DATA_PROCESSED / "propostas.csv", index=False)
transacoes.to_csv(DATA_PROCESSED / "transacoes.csv", index=False)

print("\n✅ Processamento concluído com sucesso!")


print("\n🔎 Rodando checklist de consistência...\n")

tables = {
    "agencias": agencias,
    "clientes": clientes,
    "contas": contas,
    "propostas": propostas,
    "transacoes": transacoes,
}

# 1. Verificar nulos
for name, df in tables.items():
    print(f"📂 {name}:")
    print("   - Registros:", len(df))
    print("   - Nulos por coluna:")
    print(df.isna().sum(), "\n")

# 2. Verificar unicidade de chaves primárias
print("🔑 Checando chaves primárias...\n")
if transacoes["cod_transacao"].is_unique:
    print("✅ transacoes.cod_transacao é único")
else:
    print("⚠️ transacoes.cod_transacao tem duplicados")

if contas["num_conta"].is_unique:
    print("✅ contas.num_conta é único")
else:
    print("⚠️ contas.num_conta tem duplicados")

if clientes["cod_cliente"].is_unique:
    print("✅ clientes.cod_cliente é único")
else:
    print("⚠️ clientes.cod_cliente tem duplicados")

# 3. Verificar integridade referencial
print("\n🔗 Checando chaves estrangeiras...\n")
# transacoes → contas
missing_contas = transacoes[~transacoes["num_conta"].isin(contas["num_conta"])]
print(f"🔍 Transações sem conta correspondente: {len(missing_contas)}")

# contas → clientes
missing_clientes = contas[~contas["cod_cliente"].isin(clientes["cod_cliente"])]
print(f"🔍 Contas sem cliente correspondente: {len(missing_clientes)}")

# propostas → clientes
if "cod_cliente" in propostas.columns:
    missing_clientes_prop = propostas[~propostas["cod_cliente"].isin(clientes["cod_cliente"])]
    print(f"🔍 Propostas sem cliente correspondente: {len(missing_clientes_prop)}")

# 4. Tipos de dados principais
print("\n📊 Tipos de dados por tabela:\n")
for name, df in tables.items():
    print(f"{name}:")
    print(df.dtypes, "\n")

print("\n✅ Checklist concluído!")

