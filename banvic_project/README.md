# Banvic Project

Análise de dados do BanVic (Fictício) para otimizar operações internas, melhorar a experiência do cliente e gerar recomendações práticas a partir de dados de crédito.

---

## Problema e Objetivo

O BanVic, instituição financeira nacional, realiza análises manuais de dados comerciais, marketing e CRM. O objetivo do projeto é:  

- Entender profundamente as operações e comportamentos dos clientes.  
- Otimizar operações internas e infraestrutura na nuvem com base em horários/dias de pico.  
- Apoiar decisões de marketing com segmentação de clientes em cidades onde o banco já atua.  
- Gerar insights e recomendações práticas para a diretora comercial, melhorando eficiência e experiência do cliente.

---

## Tecnologias e Versões

- **Python**  
- **Bibliotecas:** pandas, numpy, faker  
- **Requisitos:** `requirements.txt` incluso  

---

## Como Reproduzir

O projeto possui três scripts Python numerados para execução na ordem correta:  

1. `01_ingest_inspect.py` – Injestão, inspeção e carregamento dos dados.  
2. `02_clean_transform.py` – Limpeza e transformação dos dados.
3. `03_eda_and_exports.py` – Análise exploratória dos dados e preparação para dashboards.

**Setup:**

```bash
# Clonar o repositório
git clone <link-do-repo>

# Criar ambiente virtual 
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

#Baixar todos os csvs de \scriptsdatafake

# Rodar scripts na ordem
python 01_ingest_inspect.py
python 02_clean_transform.py
python 03_eda_and_exports.py


# Principais Descobertas & Recomendações
Horários e dias de pico identificados para otimizar infraestrutura e campanhas de marketing.
Análise de volume e valor médio de transações por dia da semana e por mês.
Identificação de sazonalidades e impacto de feriados/finais de semana.
Relação entre idade do cliente e uso de crédito para campanhas segmentadas.
Ranking de agências com maior e menor performance, permitindo foco em melhorias ou estratégias específicas.

(Adicionar insights do relatório posteriormente)


# Estrutura de Pastas
analise-projeto/
├─ README.md
├─ .gitignore
├─ requirements.txt       
├─ scripts/
│  ├─ 01_ingest_inspect.py
├     02_clean_transform.py         
│  └─ 03_eda_and_exports.py
├─ scriptsdatafake/
│  ├─ generate_fake_data.py                
│  └─ agencias_fake.csv
...                      #demais csvs

# Observações sobre Dados
Dados originais anonimizados utilizando Faker. A base de dados original usadas para os insights 
      é maior do que a gerada nesse projeto.
Dados simulados, não contêm informações reais de clientes.
Projeto protege a privacidade e não contém dados sensíveis reais.

#Contato 
**Ana Ju Moreira**  
Estudante de Análise e Desenvolvimento de Sistemas – UniSENAI   
- 🌐 [LinkedIn](https://www.linkedin.com/in/anajussaramoreira/)  
- 📧  ana_j_ferreira@estudante.sesisenai.org.br