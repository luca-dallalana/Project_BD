import random
from faker import Faker
import datetime

fake = Faker('pt_PT')

def generate_unique_phone_number(existing_numbers):
    while True:
        phone_number = fake.phone_number()
        if phone_number not in existing_numbers:
            existing_numbers.add(phone_number)
            return phone_number

def generate_unique_nif(existing_nifs):
    while True:
        nif = fake.numerify(text='#########')
        if nif not in existing_nifs:
            existing_nifs.add(nif)
            return nif

def generate_unique_ssn(existing_ssns):
    while True:
        ssn = fake.numerify(text='###########')
        if ssn not in existing_ssns:
            existing_ssns.add(ssn)
            return ssn

def generate_morada():
    rua = fake.street_name()
    numero = fake.building_number()
    postal_code = fake.postcode()
    cidade = fake.city()
    return f"{rua} {numero}, {postal_code} {cidade}"

existing_phone_numbers = set()
existing_nifs = set()
existing_ssns = set()
existing_consulta_sns = set()

# Generate data for clinicas
clinicas = [
    {"nome": "Clinica Lisboa", "telefone": generate_unique_phone_number(existing_phone_numbers), "morada": generate_morada()},
    {"nome": "Clinica Cascais", "telefone": generate_unique_phone_number(existing_phone_numbers), "morada": generate_morada()},
    {"nome": "Clinica Sintra", "telefone": generate_unique_phone_number(existing_phone_numbers), "morada": generate_morada()},
    {"nome": "Clinica Almada", "telefone": generate_unique_phone_number(existing_phone_numbers), "morada": generate_morada()},
    {"nome": "Clinica Oeiras", "telefone": generate_unique_phone_number(existing_phone_numbers), "morada": generate_morada()}
]

# Generate data for enfermeiros
enfermeiros = []
for clinica in clinicas:
    for _ in range(random.randint(5, 6)):
        enfermeiro = {
            "nif": generate_unique_nif(existing_nifs),
            "nome": fake.unique.name(),
            "telefone": generate_unique_phone_number(existing_phone_numbers),
            "morada": generate_morada(),
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
            "nif": generate_unique_nif(existing_nifs),
            "nome": fake.unique.name(),
            "telefone": generate_unique_phone_number(existing_phone_numbers),
            "morada": generate_morada(),
            "especialidade": especialidade
        }
        medicos.append(medico)

# Generate data for trabalha
trabalha = []
dias_da_semana = list(range(0, 7))
min_doctors_per_clinic_per_day = 8

clinica_medicos = {clinica["nome"]: [] for clinica in clinicas}
medico_clinicas = {medico["nif"]: [] for medico in medicos}

# Assign each doctor to at least two clinics
for medico in medicos:
    assigned_clinics = random.sample(clinicas, 2)
    for clinica in assigned_clinics:
        medico_clinicas[medico["nif"]].append(clinica["nome"])
        clinica_medicos[clinica["nome"]].append(medico["nif"])

# Ensure each clinic has at least 8 doctors each day
for clinica, medicos_in_clinic in clinica_medicos.items():
    while len(medicos_in_clinic) < min_doctors_per_clinic_per_day:
        medico = random.choice(medicos)
        if clinica not in medico_clinicas[medico["nif"]]:
            medico_clinicas[medico["nif"]].append(clinica)
            clinica_medicos[clinica].append(medico["nif"])

# Create the 'trabalha' entries ensuring doctors work in assigned clinics and every day
for clinica, medicos_in_clinic in clinica_medicos.items():
    for dia in dias_da_semana:
        random.shuffle(medicos_in_clinic)
        for medico_nif in medicos_in_clinic:
            trabalha.append({"nif": medico_nif, "nome": clinica, "dia_da_semana": dia})

# Generate data for pacientes
pacientes = []
for _ in range(5000):
    paciente = {
        "ssn": generate_unique_ssn(existing_ssns),
        "nif": generate_unique_nif(existing_nifs),
        "nome": fake.name(),
        "telefone": generate_unique_phone_number(existing_phone_numbers),
        "morada": generate_morada(),
        "data_nasc": fake.date_of_birth(minimum_age=0, maximum_age=100)
    }
    pacientes.append(paciente)

# Generate data for consulta
consultas = []
consultas_per_day = 20
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2024, 5, 31)
num_days = (end_date - start_date).days
date_list = [start_date + datetime.timedelta(days=x) for x in range(num_days)]

for date in date_list:
    for clinica in clinicas:
        for _ in range(consultas_per_day):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            while True:
                codigo_sns = fake.numerify(text='############')
                if codigo_sns not in existing_consulta_sns:
                    existing_consulta_sns.add(codigo_sns)
                    break
            consulta = {
                "ssn": paciente["ssn"],
                "nif": medico["nif"],
                "nome": clinica["nome"],
                "data": date,
                "hora": fake.time(),
                "codigo_sns": codigo_sns
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
