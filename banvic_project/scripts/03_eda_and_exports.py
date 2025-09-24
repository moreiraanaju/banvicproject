from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
PROC_DIR = PROJECT_ROOT / "data" / "processed"
FINAL_DIR = PROJECT_ROOT / "data" / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Carregar dados processados
# ---------------------------
trans = pd.read_csv(PROC_DIR / "transacoes.csv", parse_dates=["data_transacao"])
prop = pd.read_csv(PROC_DIR / "propostas.csv", parse_dates=["data_entrada_proposta"])
contas = pd.read_csv(PROC_DIR / "contas.csv")
agencias = pd.read_csv(PROC_DIR / "agencias.csv")
colab = pd.read_csv(PROC_DIR / "colaboradores.csv")
colab_ag = pd.read_csv(PROC_DIR / "colab_agencia.csv")

# ---------------------------
# 1) transactions_with_date_dim
# ---------------------------
transactions_with_date_dim = trans.copy()
transactions_with_date_dim.to_csv(FINAL_DIR / "transactions_with_date_dim.csv", index=False)

# ---------------------------
# 2) monthly_proposals
# ---------------------------
monthly_proposals = prop.groupby(prop["data_entrada_proposta"].dt.to_period("M")).agg(
    qtd_propostas=("cod_proposta", "count"),
    ticket_medio=("valor_proposta", "mean")
).rename_axis("year_month").reset_index()

monthly_proposals["year_month"] = monthly_proposals["year_month"].astype(str)
monthly_proposals.to_csv(FINAL_DIR / "monthly_proposals.csv", index=False)

# ---------------------------
# 3) Criar base detalhada com contas, agências e colaboradores
# ---------------------------
trans_detalhado = trans.merge(contas[["num_conta", "cod_agencia"]], on="num_conta", how="left")
trans_detalhado = trans_detalhado.merge(agencias[["cod_agencia", "nome"]], on="cod_agencia", how="left")
trans_detalhado = trans_detalhado.rename(columns={"nome": "nome_agencia"})
trans_detalhado = trans_detalhado.merge(colab_ag, on="cod_agencia", how="left")
trans_detalhado = trans_detalhado.merge(colab, on="cod_colaborador", how="left")

# 🔗 Verificação de integridade
missing_conta = trans_detalhado["cod_agencia"].isna().sum()
print(f"🔍 Transações sem conta/agência correspondente: {missing_conta}")
missing_colab = trans_detalhado["cod_colaborador"].isna().sum()
print(f"🔍 Transações sem colaborador correspondente: {missing_colab}")

# ---------------------------
# 4) Top e Bottom 3 Agências
# ---------------------------
ag_stats = trans_detalhado.groupby(["cod_agencia", "nome_agencia"]).agg(
    total_transacoes=("cod_transacao", "count"),
    valor_total=("valor_transacao", "sum")
).reset_index().sort_values("total_transacoes", ascending=False)

ag_stats.head(3).to_csv(FINAL_DIR / "top3_agencias.csv", index=False)
ag_stats.tail(3).to_csv(FINAL_DIR / "bottom3_agencias.csv", index=False)

# ---------------------------
# 5) Top colaboradores por agência
# ---------------------------
colab_stats = trans_detalhado.groupby(
    ["cod_agencia", "nome_agencia", "primeiro_nome", "ultimo_nome"]
).agg(
    total_transacoes=("cod_transacao", "count"),
    valor_total=("valor_transacao", "sum")
).reset_index()

colab_stats["full_name"] = colab_stats["primeiro_nome"] + " " + colab_stats["ultimo_nome"]
colab_stats.to_csv(FINAL_DIR / "top_colabs_per_agency.csv", index=False)

# ---------------------------
# 6) Desempenho de colaboradores (Propostas e Financiamentos)
# ---------------------------
colab_performance = (
    prop.merge(colab, on="cod_colaborador", how="left")
        .merge(colab_ag, on="cod_colaborador", how="left")
        .merge(agencias, on="cod_agencia", how="left")
        .groupby(["cod_colaborador", "primeiro_nome", "ultimo_nome", "nome"])
        .agg(
            num_propostas=("cod_proposta", "count"),
            valor_total_financiado=("valor_proposta", "sum")
        )
        .reset_index()
)

colab_performance["colaborador"] = colab_performance["primeiro_nome"] + " " + colab_performance["ultimo_nome"]
colab_performance = colab_performance.rename(columns={"nome": "nome_agencia"})

colab_performance = colab_performance[[
    "colaborador", "nome_agencia", "num_propostas", "valor_total_financiado"
]]

colab_performance.to_csv(FINAL_DIR / "colab_performance.csv", index=False)

print("✅ Exports gerados em /data/final")
