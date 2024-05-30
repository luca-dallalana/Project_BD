import random
from faker import Faker
import datetime

fake = Faker('pt_PT')

# Generate data for clinicas
clinicas = [
    {"nome": "Clinica Lisboa", "telefone": fake.unique.phone_number(), "morada": f"Rua A, 123, 1000-001 Lisboa"},
    {"nome": "Clinica Cascais", "telefone": fake.unique.phone_number(), "morada": f"Rua B, 456, 2750-001 Cascais"},
    {"nome": "Clinica Sintra", "telefone": fake.unique.phone_number(), "morada": f"Rua C, 789, 2710-001 Sintra"},
    {"nome": "Clinica Almada", "telefone": fake.unique.phone_number(), "morada": f"Rua D, 101, 2800-001 Almada"},
    {"nome": "Clinica Oeiras", "telefone": fake.unique.phone_number(), "morada": f"Rua E, 202, 2780-001 Oeiras"}
]

# Generate data for enfermeiros
enfermeiros = []
for clinica in clinicas:
    for _ in range(random.randint(5, 6)):
        enfermeiro = {
            "nif": fake.unique.numerify(text='#########'),
            "nome": fake.unique.name(),
            "telefone": fake.unique.phone_number(),
            "morada": fake.address().replace("\n", ", "),
            "nome_clinica": clinica["nome"]
        }
        enfermeiros.append(enfermeiro)

# Generate data for medicos
especialidades = ['clínica geral', 'ortopedia', 'cardiologia', 'dermatologia', 'neurologia', 'pediatria']
medicos = []
for especialidade in especialidades:
    num_medicos = 20 if especialidade == 'clínica geral' else 8
    for _ in range(num_medicos):
        medico = {
            "nif": fake.unique.numerify(text='#########'),
            "nome": fake.unique.name(),
            "telefone": fake.unique.phone_number(),
            "morada": fake.address().replace("\n", ", "),
            "especialidade": especialidade
        }
        medicos.append(medico)

# Generate data for trabalha
trabalha = []
dias_da_semana = list(range(1, 8))
for medico in medicos:
    clinicas_to_work = random.sample(clinicas, 2)
    for clinica in clinicas_to_work:
        for dia in dias_da_semana:
            trabalha.append({"nif": medico["nif"], "nome": clinica["nome"], "dia_da_semana": dia})

# Generate data for pacientes
pacientes = []
for _ in range(5000):
    paciente = {
        "ssn": fake.unique.numerify(text='###########'),
        "nif": fake.unique.numerify(text='#########'),
        "nome": fake.name(),
        "telefone": fake.phone_number(),
        "morada": fake.address().replace("\n", ", "),
        "data_nasc": fake.date_of_birth(minimum_age=0, maximum_age=100)
    }
    pacientes.append(paciente)

# Generate data for consulta
consultas = []
consultas_per_day = 20
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2024, 12, 31)
num_days = (end_date - start_date).days
date_list = [start_date + datetime.timedelta(days=x) for x in range(num_days)]

for date in date_list:
    for clinica in clinicas:
        for _ in range(consultas_per_day):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            consulta = {
                "ssn": paciente["ssn"],
                "nif": medico["nif"],
                "nome": clinica["nome"],
                "data": date,
                "hora": fake.time(),
                "codigo_sns": fake.unique.numerify(text='############')
            }
            consultas.append(consulta)

# Generate data for receita
receitas = []
for consulta in consultas:
    if random.random() < 0.8:
        num_medicamentos = random.randint(1, 6)
        for _ in range(num_medicamentos):
            receita = {
                "codigo_sns": consulta["codigo_sns"],
                "medicamento": fake.word(),
                "quantidade": random.randint(1, 3)
            }
            receitas.append(receita)

# Generate data for observacao
observacoes = []
parametros_sintomas = [f"Sintoma {i}" for i in range(1, 51)]
parametros_metricas = [f"Metrica {i}" for i in range(1, 21)]

for consulta in consultas:
    num_sintomas = random.randint(1, 5)
    num_metricas = random.randint(0, 3)
    
    for _ in range(num_sintomas):
        observacao = {
            "id": consulta["codigo_sns"],
            "parametro": random.choice(parametros_sintomas),
            "valor": None
        }
        observacoes.append(observacao)
    
    for _ in range(num_metricas):
        observacao = {
            "id": consulta["codigo_sns"],
            "parametro": random.choice(parametros_metricas),
            "valor": round(random.uniform(1.0, 100.0), 2)
        }
        observacoes.append(observacao)

# SQL query generation functions
def generate_insert_query(table, data):
    columns = ", ".join(data[0].keys())
    values_list = []
    for row in data:
        values = ", ".join(f"'{str(value).replace('\'', '\'\'')}'" if value is not None else 'NULL' for value in row.values())
        values_list.append(f"({values})")
    values_str = ",\n".join(values_list)
    return f"INSERT INTO {table} ({columns}) VALUES\n{values_str};\n"

# Generate SQL insert statements
queries = []
queries.append(generate_insert_query('clinica', clinicas))
queries.append(generate_insert_query('enfermeiro', enfermeiros))
queries.append(generate_insert_query('medico', medicos))
queries.append(generate_insert_query('trabalha', trabalha))
queries.append(generate_insert_query('paciente', pacientes))
queries.append(generate_insert_query('consulta', consultas))
queries.append(generate_insert_query('receita', receitas))
queries.append(generate_insert_query('observacao', observacoes))

# Write to a file
with open('populate_database.sql', 'w') as file:
    for query in queries:
        file.write(query)
