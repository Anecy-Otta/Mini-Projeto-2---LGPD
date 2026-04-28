# Mini Projeto 2 - LGPD

Este projeto faz parte da disciplina de Linguagem de Programação 2 da FATEC Rio Claro. O objetivo é aplicar os conceitos da Lei Geral de Proteção de Dados (LGPD) em um banco de dados de usuários.

## Tecnologias Utilizadas
* Python
* SQLAlchemy (ORM)
* PostgreSQL

## Atividades Desenvolvidas
- [x] **Atividade 1:** Anonimização de dados sensíveis (Nome, CPF, E-mail e Telefone) utilizando máscaras de caracteres.
- [x] **Atividade 2:** Exportação de registros anonimizados em arquivos CSV/XLS por ano de nascimento.
- [ ] **Atividade 3:** Exportação geral de dados (Nome e CPF) sem anonimização.
- [ ] **Atividade 4:** Mensuração de tempo de execução e logs.

## Como executar o projeto
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   
2. Execute o script principal:
   ```bash
   python LGPD.py