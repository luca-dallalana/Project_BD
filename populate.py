from faker import Faker
from datetime import datetime, timedelta, date
import random

# Initialize Faker for Portuguese (Portugal)
fake = Faker('pt_PT')

codigo_sns = 0
id_consulta = 0
# Funções auxiliares
def gerar_data_nasc():
    return str(fake.date_of_birth(minimum_age=18, maximum_age=90))

def gerar_morada():
    city = fake.city()
    return f"{fake.street_address()} {random.randint(1000,9999)}-{random.randint(100,999)} {city}".replace("'", "")

def gerar_data_consulta(ano):
    start_date = date(ano, 1, 1)
    end_date = date(ano, 12, 31)
    return fake.date_between(start_date, end_date)

def gerar_hora_consulta():
    if random.choice([True, False]):
        horas = random.randint(8, 12)
    else:
        horas = random.randint(14, 18)
    if horas == 8:
        horas = '08'
    if horas == 9:
        horas = '09'
    minutos_options = ('00','30')
    minutos = random.choice(minutos_options)
    hora = f"{horas}:{minutos}:00"
    return hora

# Função para gerar dados para a tabela 'clinica'
def gerar_clinicas():
    clinicas = []
    localidades = ['Lisboa', 'Sintra', 'Cascais']
    i = 0
    for _ in range(5):
        nome = 'clinica ' + fake.company()
        telefone = fake.msisdn()
        morada = f"{fake.street_address()} {random.randint(1000,9999)}-{random.randint(100,999)} {localidades[i]}".replace("'", "")
        clinicas.append((nome, telefone, morada))
        i += 1
        if i == 3:
            i = 0
    return clinicas

# Função para gerar dados para a tabela 'enfermeiro'
def gerar_enfermeiros(clinicas):
    enfermeiros = []
    for clinica in clinicas:
        for _ in range(random.randint(5, 6)):
            while True:
                nif = fake.unique.random_number(digits=9)
                if len(str(nif)) == 9:
                    break
            nome = fake.unique.name()
            telefone = fake.msisdn()
            morada = gerar_morada()
            nome_clinica = clinica[0]
            enfermeiros.append((nif, nome, telefone, morada, nome_clinica))
    return enfermeiros

# Função para gerar dados para a tabela 'medico'
def gerar_medicos():
    especialidades = ['ortopedia', 'cardiologia', 'dermatologia', 'pediatria', 'neurologia']
    medicos = []
    for _ in range(20):
        while True:
            nif = fake.unique.random_number(digits=9)
            if len(str(nif)) == 9:
                break
        nome = fake.unique.name()
        telefone = fake.msisdn()
        morada = gerar_morada()
        especialidade = 'clínica geral'
        medicos.append((nif, nome, telefone, morada, especialidade))
    for _ in range(40):
        while True:
            nif = fake.unique.random_number(digits=9)
            if len(str(nif)) == 9:
                 break
        nome = fake.unique.name()
        telefone = fake.msisdn()
        morada = gerar_morada()
        especialidade = random.choice(especialidades)
        medicos.append((nif, nome, telefone, morada, especialidade))
    return medicos

def gerar_trabalha(medicos, clinicas):
    trabalha = []
    dias_da_semana = list(range(0, 7))
    
    for c in range(1,5):#1,2,3,4
       for m in range(12):
        for dia in dias_da_semana[:4]:
            trabalha.append((medicos[m + 12*(c-1)][0], clinicas[c - 1][0], dia))
        for dia in dias_da_semana[4:]:
            trabalha.append((medicos[m + 12*(c-1)][0], clinicas[c][0], dia))
    
    for m in range(48,60):
        for dia in dias_da_semana[:4]:
            trabalha.append((medicos[m][0], clinicas[4][0], dia))
        for dia in dias_da_semana[4:]:
            trabalha.append((medicos[m][0], clinicas[0][0], dia))

    return trabalha

# Função para gerar dados para a tabela 'paciente'
def gerar_pacientes():
    pacientes = []
    for _ in range(5000):
        while True:
            nif = fake.unique.random_number(digits=9)
            ssn = fake.unique.random_number(digits=11)
            if len(str(nif)) == 9 and len(str(ssn)) == 11:
                break
        nome = fake.name()
        telefone = fake.msisdn()
        morada = gerar_morada()
        data_nasc = gerar_data_nasc()
        pacientes.append((ssn, nif, nome, telefone, morada, data_nasc))
    return pacientes

# Função para gerar dados para a tabela 'consulta'
def gerar_consultas(pacientes, medicos, clinicas, ano):
    data_inicio = datetime(ano, 1, 1)
    # Data de término do ano (último dia do ano)
    data_fim = datetime(ano, 12, 31)
    data_hoje = datetime(2024, 5, 31)

    # Lista para armazenar todas as datas
    lista_de_datas = []

    # Loop para iterar do início ao fim do ano
    if ano == 2023:
        while data_inicio <= data_fim:
            # Adiciona a data formatada à lista
            lista_de_datas.append(data_inicio.strftime('%Y-%m-%d'))
            # Avança para o próximo dia
            data_inicio += timedelta(days=1)
    if ano == 2024:
        while data_inicio <= data_hoje:
            # Adiciona a data formatada à lista
            lista_de_datas.append(data_inicio.strftime('%Y-%m-%d'))
            # Avança para o próximo dia
            data_inicio += timedelta(days=1)


    consultas = []
    i = 0
    for data in lista_de_datas:
        ssn_usado = []
        for medico in medicos:
            horas_usadas = []
            for _ in range(2):
                ssn = pacientes[i][0]
                i += 1
                if i == 5000:
                    i -= 1
                    while True:
                        ssn = random.choice(pacientes)[0]
                        if ssn not in ssn_usado:
                            ssn_usado.append(ssn)
                            break
                data_formatada = datetime.strptime(str(data), '%Y-%m-%d')
                dia_da_semana = (data_formatada.weekday() + 1) % 7
                nif = medico[0]
                clinica = [tuplo for tuplo in trabalhas if tuplo[0] == medico[0] and tuplo[2] == dia_da_semana][0][1]
                while True:
                    hora = gerar_hora_consulta()
                    if hora not in horas_usadas:
                        horas_usadas.append(hora)
                        break
                while True:
                    codigo_sns = fake.unique.random_number(digits=12)
                    if len(str(codigo_sns)) == 12:
                        break
                global id_consulta
                id_consulta += 1
                consultas.append((id_consulta ,ssn, nif, clinica, data, hora, codigo_sns))
    return consultas

# Função para gerar dados para a tabela 'receita'
def gerar_receitas(consultas):
    receitas = []
    medicamentos = ['Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Atorvastatina', 'Metformina', 'losartan']
    for consulta in consultas:
        if random.random() < 0.8:
            medicamentos_usados = []
            for _ in range(random.randint(1, 6)):
                codigo_sns = consulta[6]
                while True:
                    medicamento = random.choice(medicamentos)
                    if medicamento not in medicamentos_usados:
                        medicamentos_usados.append(medicamento)
                        break
                quantidade = random.randint(1, 3)
                receitas.append((codigo_sns, medicamento, quantidade))
    return receitas

# Função para gerar dados para a tabela 'observacao'
def gerar_observacoes(consultas):
    observacoes = []
    sintomas = [f'Sintoma{i}' for i in range(1, 51)]
    metricas = [f'Metrica{i}' for i in range(1, 21)]
    for consulta in consultas:
        id_consulta = consulta[0]
        parametros_usados = []
        for _ in range(random.randint(1, 5)):
            while True:
                parametro = random.choice(sintomas)
                if parametro not in parametros_usados:
                    parametros_usados.append(parametro)
                    break
            observacoes.append((id_consulta, parametro))
        for _ in range(random.randint(0, 3)):
            while True:
                parametro = random.choice(metricas)
                if parametro not in parametros_usados:
                    parametros_usados.append(parametro)
                    break
            valor = round(random.uniform(0, 100), 4)
            observacoes.append((id_consulta, parametro, valor))
    return observacoes

clinicas = gerar_clinicas()
enfermeiros = gerar_enfermeiros(clinicas)
medicos = gerar_medicos()
trabalhas = gerar_trabalha(medicos, clinicas)
pacientes = gerar_pacientes()
consultas_2023 = gerar_consultas(pacientes, medicos, clinicas, 2023)
consultas_2024 = gerar_consultas(pacientes, medicos, clinicas, 2024)
receitas_2023 = gerar_receitas(consultas_2023)
receitas_2024 = gerar_receitas(consultas_2024)
observacoes_2023 = gerar_observacoes(consultas_2023)
observacoes_2024 = gerar_observacoes(consultas_2024)

values = []
for clinica in clinicas:
    values.append(f"insert into clinica values ('{clinica[0]}', '{clinica[1]}', '{clinica[2]}');")
values.append('\n')

for enfermeiro in enfermeiros:
    values.append(f"insert into enfermeiro values ('{enfermeiro[0]}', '{enfermeiro[1]}', '{enfermeiro[2]}', '{enfermeiro[3]}', '{enfermeiro[4]}');")
values.append('\n')

for medico in medicos:
    values.append(f"insert into medico values ('{medico[0]}', '{medico[1]}', '{medico[2]}', '{medico[3]}', '{medico[4]}');")
values.append('\n')

for trabalha in trabalhas:
    values.append(f"insert into trabalha values ('{trabalha[0]}', '{trabalha[1]}', '{trabalha[2]}');")
values.append('\n')

for paciente in pacientes:
    values.append(f"insert into paciente values ('{paciente[0]}', '{paciente[1]}', '{paciente[2]}', '{paciente[3]}', '{paciente[4]}', '{paciente[5]}');")
values.append('\n')

for consulta in consultas_2023:
    values.append(f"insert into consulta values ('{consulta[0]}', '{consulta[1]}', '{consulta[2]}', '{consulta[3]}', '{consulta[4]}', '{consulta[5]}', '{consulta[6]}');")
values.append('\n')

for consulta in consultas_2024:
    values.append(f"insert into consulta values ('{consulta[0]}', '{consulta[1]}', '{consulta[2]}', '{consulta[3]}', '{consulta[4]}', '{consulta[5]}', '{consulta[6]}');")
values.append('\n')

for receita in receitas_2023:
    values.append(f"insert into receita values ('{receita[0]}', '{receita[1]}', '{receita[2]}');")
values.append('\n')

for receita in receitas_2024:
    values.append(f"insert into receita values ('{receita[0]}', '{receita[1]}', '{receita[2]}');")
values.append('\n')

for observacao in observacoes_2023:
    if len(observacao) == 3:
        values.append(f"insert into observacao values ('{observacao[0]}', '{observacao[1]}', '{observacao[2]}');")
    else:
        values.append(f"insert into observacao values ('{observacao[0]}', '{observacao[1]}');")

for observacao in observacoes_2024:
    if len(observacao) == 3:
        values.append(f"insert into observacao values ('{observacao[0]}', '{observacao[1]}', '{observacao[2]}');")
    else:
        values.append(f"insert into observacao values ('{observacao[0]}', '{observacao[1]}');")

# Write the SQL statements to a file
with open('populate.sql', 'w') as file:
    for value in values:
        file.write(value + '\n')
