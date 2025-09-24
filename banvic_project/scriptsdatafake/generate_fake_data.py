import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)

# ------------------- Funções auxiliares -------------------

def gerar_cpf():
    return fake.cpf()

def gerar_cnpj():
    return fake.cnpj()

def gerar_data(inicio="2010-01-01", fim="2023-12-31", com_hora=False, com_micro=False):
    start = datetime.strptime(inicio, "%Y-%m-%d")
    end = datetime.strptime(fim, "%Y-%m-%d")
    delta = end - start
    aleatorio = start + timedelta(days=random.randint(0, delta.days),
                                  seconds=random.randint(0, 86400))

    if com_hora:
        if com_micro:
            return aleatorio.strftime("%Y-%m-%d %H:%M:%S.%f UTC")
        return aleatorio.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        return aleatorio.strftime("%Y-%m-%d")

def gerar_cep():
    cep = fake.postcode()
    return cep if random.random() < 0.5 else cep.replace("-", "")

def gerar_float(min_val=10, max_val=200000):
    return float(f"{random.uniform(min_val, max_val):.15f}")

# ------------------- Tabelas -------------------

def gerar_agencias(qtd=10):
    agencias = []
    tipos = ["Física", "Digital"]
    cidades = ["São Paulo", "Campinas", "Osasco", "Porto Alegre",
               "Rio de Janeiro", "Florianópolis", "Recife", "Curitiba"]

    for i in range(1, qtd + 1):
        agencia = {
            "cod_agencia": i,
            "nome": f"Agência {fake.city()}",
            "endereco": fake.address().replace("\n", " "),
            "cidade": random.choice(cidades),
            "uf": fake.estado_sigla(),
            "data_abertura": gerar_data("2010-01-01", "2023-12-31"),
            "tipo_agencia": random.choice(tipos)
        }
        agencias.append(agencia)
    return agencias

def gerar_clientes(qtd=100):
    clientes = []
    for i in range(1, qtd + 1):
        tipo = random.choice(["PF", "PJ"])
        if tipo == "PF":
            doc = gerar_cpf()
            data_nasc = gerar_data("1940-01-01", "2005-12-31", com_hora=False)
        else:
            doc = gerar_cnpj()
            data_nasc = ""

        cliente = {
            "cod_cliente": i,
            "primeiro_nome": fake.first_name(),
            "ultimo_nome": fake.last_name(),
            "email": fake.email(),
            "tipo_cliente": tipo,
            "data_inclusao": gerar_data("2015-01-01", "2023-12-31", com_hora=True),
            "cpfcnpj": doc,
            "data_nascimento": data_nasc,
            "endereco": fake.address().replace("\n", " "),
            "cep": gerar_cep()
        }
        clientes.append(cliente)
    return clientes

def gerar_colaboradores(qtd=30):
    colaboradores = []
    for i in range(1, qtd + 1):
        colab = {
            "cod_colaborador": i,
            "primeiro_nome": fake.first_name(),
            "ultimo_nome": fake.last_name(),
            "email": fake.email(),
            "cpf": gerar_cpf(),
            "data_nascimento": gerar_data("1950-01-01", "2000-12-31", com_hora=False),
            "endereco": fake.address().replace("\n", " "),
            "cep": gerar_cep()
        }
        colaboradores.append(colab)
    return colaboradores

def gerar_colaborador_agencia(colaboradores, agencias):
    vinculos = []
    for colab in colaboradores:
        vinculo = {
            "cod_colaborador": colab["cod_colaborador"],
            "cod_agencia": random.choice(agencias)["cod_agencia"]
        }
        vinculos.append(vinculo)
    return vinculos

def gerar_contas(clientes, agencias, colaboradores, qtd=200):
    contas = []
    for i in range(1, qtd + 1):
        cliente = random.choice(clientes)
        agencia = random.choice(agencias)
        colaborador = random.choice(colaboradores)
        conta = {
            "num_conta": i,
            "cod_cliente": cliente["cod_cliente"],
            "cod_agencia": agencia["cod_agencia"],
            "cod_colaborador": colaborador["cod_colaborador"],
            "tipo_conta": cliente["tipo_cliente"],
            "data_abertura": gerar_data("2010-01-01", "2022-12-31", com_hora=True),
            "saldo_total": gerar_float(),
            "saldo_disponivel": gerar_float(),
            "data_ultimo_lancamento": gerar_data("2010-01-01", "2023-12-31", com_hora=True, com_micro=True)
        }
        contas.append(conta)
    return contas

def gerar_propostas(clientes, colaboradores, qtd=50):
    propostas = []
    status_opts = ["Enviada", "Aprovada", "Rejeitada"]
    for i in range(1, qtd + 1):
        cliente = random.choice(clientes)
        colab = random.choice(colaboradores)
        valor_proposta = gerar_float(1000, 200000)
        valor_entrada = valor_proposta * random.uniform(0.1, 0.4)
        valor_financiamento = valor_proposta + valor_entrada
        taxa = round(random.uniform(0.01, 0.03), 4)
        qtd_parcelas = random.choice([12, 24, 36, 48, 60, 100])
        proposta = {
            "cod_proposta": i,
            "cod_cliente": cliente["cod_cliente"],
            "cod_colaborador": colab["cod_colaborador"],
            "data_entrada_proposta": gerar_data("2010-01-01", "2023-12-31", com_hora=True),
            "taxa_juros_mensal": taxa,
            "valor_proposta": valor_proposta,
            "valor_financiamento": valor_financiamento,
            "valor_entrada": valor_entrada,
            "valor_prestacao": valor_financiamento / qtd_parcelas,
            "quantidade_parcelas": qtd_parcelas,
            "carencia": random.randint(0, 6),
            "status_proposta": random.choice(status_opts)
        }
        propostas.append(proposta)
    return propostas

def gerar_transacoes(contas, qtd=200):
    transacoes = []
    tipos = ["Saque", "Depósito", "Transferência", "Pagamento"]
    for i in range(1, qtd + 1):
        conta = random.choice(contas)
        valor = random.uniform(10, 5000)
        if random.random() < 0.5:
            valor = -valor  # saque/pagamento negativo
        transacao = {
            "cod_transacao": i,
            "num_conta": conta["num_conta"],
            "data_transacao": gerar_data("2015-01-01", "2023-12-31", com_hora=True, com_micro=random.random() < 0.3),
            "nome_transacao": random.choice(tipos),
            "valor_transacao": round(valor, 2)
        }
        transacoes.append(transacao)
    return transacoes

# ------------------- Função de salvar -------------------

def salvar_csv(nome_arquivo, lista, campos):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(lista)

# ------------------- Execução -------------------

agencias = gerar_agencias(10)
clientes = gerar_clientes(100)
colaboradores = gerar_colaboradores(30)
colab_agencia = gerar_colaborador_agencia(colaboradores, agencias)
contas = gerar_contas(clientes, agencias, colaboradores, 200)
propostas = gerar_propostas(clientes, colaboradores, 50)
transacoes = gerar_transacoes(contas, 300)

salvar_csv("agencias_fake.csv", agencias,
           ["cod_agencia","nome","endereco","cidade","uf","data_abertura","tipo_agencia"])

salvar_csv("clientes_fake.csv", clientes,
           ["cod_cliente","primeiro_nome","ultimo_nome","email","tipo_cliente",
            "data_inclusao","cpfcnpj","data_nascimento","endereco","cep"])

salvar_csv("colaboradores_fake.csv", colaboradores,
           ["cod_colaborador","primeiro_nome","ultimo_nome","email","cpf","data_nascimento","endereco","cep"])

salvar_csv("colaborador_agencia_fake.csv", colab_agencia,
           ["cod_colaborador","cod_agencia"])

salvar_csv("contas_fake.csv", contas,
           ["num_conta","cod_cliente","cod_agencia","cod_colaborador","tipo_conta",
            "data_abertura","saldo_total","saldo_disponivel","data_ultimo_lancamento"])

salvar_csv("propostas_credito_fake.csv", propostas,
           ["cod_proposta","cod_cliente","cod_colaborador","data_entrada_proposta","taxa_juros_mensal",
            "valor_proposta","valor_financiamento","valor_entrada","valor_prestacao","quantidade_parcelas",
            "carencia","status_proposta"])

salvar_csv("transacoes_fake.csv", transacoes,
           ["cod_transacao","num_conta","data_transacao","nome_transacao","valor_transacao"])

print("✅ Arquivos gerados com sucesso!")
