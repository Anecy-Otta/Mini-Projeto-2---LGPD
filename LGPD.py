import csv
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import time
from functools import wraps
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    """
    Atividade 1: Ajuste para anonimizar campos sensíveis 
    """
    dados = list(row)

    nome_original = dados[1]
    partes_nome = nome_original.split(' ')
    primeiro_nome = partes_nome[0]
    anonimo = primeiro_nome[0] + ('*' * (len(primeiro_nome) - 1))
    if len(partes_nome) > 1:
        dados[1] = anonimo + " " + " ".join(partes_nome[1:])
    else:
        dados[1] = anonimo

    dados[2] = f"{dados[2][:4]}*** ***-**"

    email = dados[3]
    prefixo, dominio = email.split('@')
    dados[3] = f"{prefixo[0]}{'*' * (len(prefixo) - 1)}@{dominio}"

    telefone = dados[4]
    dados[4] = telefone[-4:]

    return tuple(dados)

@medir_tempo
def exportar_por_ano(lista_usuarios):
    """
    Atividade 2: Agrupa usuários por ano e gera ficheiros CSV individuais.
    """
    dados_por_ano = {}

    for user in lista_usuarios:
        ano_nascimento = user[5].year
        
        if ano_nascimento not in dados_por_ano:
            dados_por_ano[ano_nascimento] = []
        
        dados_por_ano[ano_nascimento].append(user)

    for ano, registros in dados_por_ano.items():
        nome_arquivo = f"{ano}.csv"
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
            escritor.writerows(registros)
            
    print(f" Gerados {len(dados_por_ano)} ficheiros CSV.")

@medir_tempo
def exportar_geral_original(engine):
    """
    Atividade 3: Gera um relatório com Nome e CPF originais (sem anonimização).
    """
    with engine.connect() as conn:
        print("Gerando relatório geral (Nome/CPF)...")
        result = conn.execute(text("SELECT nome, cpf FROM usuarios;"))
        
        with open('todos.csv', 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['nome', 'cpf'])
            escritor.writerows(result)
            
    print("Atividade 3 concluída: Arquivo 'todos.csv' gerado.")

users_anonimos = []

with engine.connect() as conn:
    print("A procurar dados no banco...")
    result = conn.execute(text("SELECT * FROM usuarios;"))
    
    for row in result:
        row_protegida = LGPD(row)
        users_anonimos.append(row_protegida)

print("\n--- Amostra dos dados anonimizados ---")
for user in users_anonimos[:5]:
    print(user)

exportar_por_ano(users_anonimos)

exportar_geral_original(engine)