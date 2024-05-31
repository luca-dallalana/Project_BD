import random
from faker import Faker
import datetime
fake = Faker('pt_PT')

Telefone = 100000000000000
Morada = 0
NIF = 100000000
SSN = 10000000000
SNS = 100000000000


start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2024, 5, 31)
time_slots = ['8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30']

def create_timetable(dict):
    current_date = start_date
    while current_date <= end_date:
        dict[str(current_date)] = time_slots
        current_date += datetime.timedelta(days=1)

date_clinica_lisboa = create_timetable()

# Generate data for clinicas
clinicas = [
    {"nome": "Clinica Lisboa", "telefone": Telefone + 1, "morada": 'Rua A' + str(Morada + 1)},
    {"nome": "Clinica Cascais", "telefone": Telefone + 2, "morada": 'Rua A' + str(Morada + 2)},
    {"nome": "Clinica Sintra", "telefone": Telefone + 3, "morada": 'Rua A' + str(Morada + 3)},
    {"nome": "Clinica Almada", "telefone": Telefone + 4, "morada": 'Rua A' + str(Morada + 4)},
    {"nome": "Clinica Oeiras", "telefone": Telefone + 5, "morada": 'Rua A' + str(Morada + 5)}
]

Telefone += 6
Morada += 6

# Generate data for enfermeiros
enfermeiros = []
for clinica in clinicas:
    for _ in range(random.randint(5, 6)):
        enfermeiro = {
            "nif": NIF,
            "nome": 'Enfermeiro' + str(NIF),
            "telefone": Telefone,
            "morada": 'Rua B' + str(Morada),
            "nome_clinica": clinica["nome"]
        }
        NIF += 1
        Telefone += 1
        Morada += 1
        enfermeiros.append(enfermeiro)

# Generate data for medicos
especialidades = ['clínica geral', 'ortopedia', 'cardiologia', 'dermatologia', 'neurologia', 'pediatria']
medicos = []
for especialidade in especialidades:
    num_medicos = 20 if especialidade == 'clínica geral' else 8
    for _ in range(num_medicos):
        medico = {
            "nif": NIF,
            "nome": 'Medico' + str(NIF),
            "telefone": Telefone,
            "morada": 'Rua C' + str(Morada),
            "especialidade": especialidade,
            "consultations_per_day": 0  # Track the number of consultations per day for each doctor
        }
        NIF += 1
        Telefone += 1
        Morada += 1
        medicos.append(medico)

# Generate data for pacientes
pacientes = []
for _ in range(5000):
    paciente = {
        "ssn": SSN,
        "nif": NIF,
        "nome": 'Paciente' + str(NIF),
        "telefone": Telefone,
        "morada": 'Rua D' + str(Morada),
        "data_nasc": fake.date_of_birth(minimum_age=0, maximum_age=100)
    }
    NIF += 1
    Telefone += 1
    Morada += 1
    SSN += 1
    pacientes.append(paciente)

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

# Ensure each clinic has at least 8 doctors each day and doctors work in only one clinic per day
for clinica, medicos_in_clinic in clinica_medicos.items():
    for dia in dias_da_semana:
        available_doctors = medicos_in_clinic.copy()
        while len(available_doctors) < min_doctors_per_clinic_per_day:
            medico = random.choice(medicos)
            if clinica not in medico_clinicas[medico["nif"]]:
                medico_clinicas[medico["nif"]].append(clinica)
                clinica_medicos[clinica].append(medico["nif"])
                available_doctors.append(medico["nif"])
        
        random.shuffle(available_doctors)
        for medico_nif in available_doctors[:min_doctors_per_clinic_per_day]:
            trabalha.append({"nif": medico_nif, "nome": clinica, "dia_da_semana": dia})

# Ensure no doctor works in different clinics on the same day
for medico_nif, clinics in medico_clinicas.items():
    clinic_schedule = {}
    for dia in dias_da_semana:
        clinic = random.choice(clinics)
        while dia in clinic_schedule and clinic in clinic_schedule[dia]:
            clinic = random.choice(clinics)
        if dia not in clinic_schedule:
            clinic_schedule[dia] = []
        clinic_schedule[dia].append(clinic)
        trabalha.append({"nif": medico_nif, "nome": clinic, "dia_da_semana": dia})

# Generate data for consulta
consultas = []
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2024, 5, 31)
num_days = (end_date - start_date).days
date_list = [start_date + datetime.timedelta(days=x) for x in range(num_days)]

for date in date_list:
    for clinica in clinicas:
        while True:
            consultations_count = len([c for c in consultas if c["nome"] == clinica["nome"] and c["data"] == date])
            if consultations_count >= 20:
                break
            available_doctors = [medico for medico in medicos if clinica["nome"] in medico_clinicas[medico["nif"]]]
            random.shuffle(available_doctors)
            for medico in available_doctors:
                if medico["consultations_per_day"] < 2:
                    paciente = random.choice(pacientes)
                    codigo_sns = SNS
                    hour = random.choice([8,9,10,11,12,14,15,16,17,18])
                    minute = random.choice([0,30])
                    SNS += 1
                    if (8 <= hour < 13 or 14 <= hour < 19) and (minute == 0 or minute == 30):
                        if paciente["nif"] != medico["nif"]:
                            day_of_week = date.weekday()
                            if clinica["nome"] in medico_clinicas[medico["nif"]] and trabalha.count({"nif": medico["nif"], "nome": clinica["nome"], "dia_da_semana": day_of_week}) > 0:
                                consulta = {
                                    "ssn": paciente["ssn"],
                                    "nif": medico["nif"],
                                    "nome": clinica["nome"],
                                    "data": date,
                                    "hora": hour,
                                    "codigo_sns": codigo_sns
                                }
                                consultas.append(consulta)
                                medico["consultations_per_day"] += 1
                                break

# Reset consultations count for each doctor at the end of the day
for medico in medicos:
    medico["consultations_per_day"] = 0

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

# SQL query generation functions
def generate_insert_query(table, data):
    columns = ", ".join(data[0].keys())
    values_list = []
    for row in data:
        values = ", ".join("'" + str(value).replace("'", "''") + "'" if value is not None else 'NULL' for value in row.values())
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
