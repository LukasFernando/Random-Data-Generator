import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Inicializa o gerador de dados falsos
fake = Faker()

# Função para gerar dados aleatórios para a tabela 'users'
def gerar_users(num_linhas):
    dados = {
        'id': [i + 1 for i in range(num_linhas)],
        'name': [fake.name() for _ in range(num_linhas)],
        'email': [fake.email() for _ in range(num_linhas)],
        'password': [fake.password() for _ in range(num_linhas)],
        'created_on': [fake.date_this_decade() for _ in range(num_linhas)],
        'updated_on': [fake.date_this_decade() for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'dim_candidates'
def gerar_dim_candidates(num_linhas):
    dados = {
        'candidate_id': [i + 1 for i in range(num_linhas)],
        'candidate_name': [fake.name() for _ in range(num_linhas)],
        'email': [fake.email() for _ in range(num_linhas)],
        'phone': [fake.phone_number()[:13] for _ in range(num_linhas)],
        'birth_date': [fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d') for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'dim_jobs'
def gerar_dim_jobs(num_linhas):
    dados = {
        'job_id': [i + 1 for i in range(num_linhas)],
        'job_title': [fake.job() for _ in range(num_linhas)],
        'number_of_positions': [random.randint(1, 10) for _ in range(num_linhas)],
        'job_requirements': [fake.text(max_nb_chars=500) for _ in range(num_linhas)],
        'job_status': [random.choice(['Open', 'Closed']) for _ in range(num_linhas)],
        'location': [fake.city() for _ in range(num_linhas)],
        'responsible_person': [fake.name() for _ in range(num_linhas)],
        'opening_date': [fake.date_time_this_year() for _ in range(num_linhas)],
        'closing_date': [fake.date_time_this_year() + timedelta(days=random.randint(1, 30)) for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'dim_recruitment_processes'
def gerar_dim_recruitment_processes(num_linhas):
    dados = {
        'process_id': [i + 1 for i in range(num_linhas)],
        'process_name': [fake.word() for _ in range(num_linhas)],
        'start_date': [fake.date_time_this_year() for _ in range(num_linhas)],
        'end_date': [fake.date_time_this_year() + timedelta(days=random.randint(1, 30)) for _ in range(num_linhas)],
        'process_status': [random.choice(['Active', 'Completed', 'Pending']) for _ in range(num_linhas)],
        'description_processes': [fake.text(max_nb_chars=500) for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'dim_recruiters'
def gerar_dim_recruiters(num_linhas):
    dados = {
        'recruiter_id': [i + 1 for i in range(num_linhas)],
        'recruiter_name': [fake.name() for _ in range(num_linhas)],
        'role': [fake.job() for _ in range(num_linhas)],
        'feedbacks_given': [random.randint(0, 100) for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'fact_applications'
def gerar_fact_applications(num_linhas, num_candidates, num_jobs, num_processes, num_recruiters):
    dados = {
        'recruiter_id': [random.randint(1, num_recruiters) for _ in range(num_linhas)],
        'candidate_id': [random.randint(1, num_candidates) for _ in range(num_linhas)],
        'job_id': [random.randint(1, num_jobs) for _ in range(num_linhas)],
        'process_id': [random.randint(1, num_processes) for _ in range(num_linhas)],
        'number_of_applications': [random.randint(1, 10) for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Função para gerar dados aleatórios para a tabela 'fact_hirings'
def gerar_fact_hirings(num_linhas, num_candidates, num_jobs):
    dados = {
        'hiring_id': [i + 1 for i in range(num_linhas)],
        'candidate_id': [random.randint(1, num_candidates) for _ in range(num_linhas)],
        'job_id': [random.randint(1, num_jobs) for _ in range(num_linhas)],
        'hiring_date': [fake.date_this_year() for _ in range(num_linhas)],
        'initial_salary': [round(random.uniform(30000, 100000), 2) for _ in range(num_linhas)],
        'contract_type': [random.choice(['Full-time', 'Part-time', 'Contract']) for _ in range(num_linhas)],
        'acceptance_date': [fake.date_time_this_year() for _ in range(num_linhas)]
    }
    return pd.DataFrame(dados)

# Criar um objeto ExcelWriter para salvar várias planilhas
with pd.ExcelWriter('dados.xlsx', engine='openpyxl') as writer:
    # Definir o número de registros para cada tabela
    num_registros = {
        'users': 100,
        'dim_candidates': 50,
        'dim_jobs': 20,
        'dim_recruitment_processes': 15,
        'dim_recruiters': 10,
        'fact_applications': 200,
        'fact_hirings': 100
    }
    
    # Gerar e salvar os dados para cada tabela
    df_users = gerar_users(num_registros['users'])
    df_users.to_excel(writer, sheet_name='users', index=False)
    
    df_dim_candidates = gerar_dim_candidates(num_registros['dim_candidates'])
    df_dim_candidates.to_excel(writer, sheet_name='dim_candidates', index=False)
    
    df_dim_jobs = gerar_dim_jobs(num_registros['dim_jobs'])
    df_dim_jobs.to_excel(writer, sheet_name='dim_jobs', index=False)
    
    df_dim_recruitment_processes = gerar_dim_recruitment_processes(num_registros['dim_recruitment_processes'])
    df_dim_recruitment_processes.to_excel(writer, sheet_name='dim_recruitment_processes', index=False)
    
    df_dim_recruiters = gerar_dim_recruiters(num_registros['dim_recruiters'])
    df_dim_recruiters.to_excel(writer, sheet_name='dim_recruiters', index=False)
    
    df_fact_applications = gerar_fact_applications(
        num_registros['fact_applications'], 
        num_registros['dim_candidates'], 
        num_registros['dim_jobs'], 
        num_registros['dim_recruitment_processes'], 
        num_registros['dim_recruiters']
    )
    df_fact_applications.to_excel(writer, sheet_name='fact_applications', index=False)
    
    df_fact_hirings = gerar_fact_hirings(num_registros['fact_hirings'], num_registros['dim_candidates'], num_registros['dim_jobs'])
    df_fact_hirings.to_excel(writer, sheet_name='fact_hirings', index=False)

print("Arquivo Excel criado com dados!")
