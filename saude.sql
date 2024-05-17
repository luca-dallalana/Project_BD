-- Drop existing tables if they exist
DROP TABLE IF EXISTS clinica CASCADE;
DROP TABLE IF EXISTS enfermeiro CASCADE;
DROP TABLE IF EXISTS medico CASCADE;
DROP TABLE IF EXISTS trabalha CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS receita CASCADE;
DROP TABLE IF EXISTS consulta CASCADE;
DROP TABLE IF EXISTS sintoma CASCADE;
DROP TABLE IF EXISTS observacao CASCADE;

-- Create the tables
CREATE TABLE clinica(
    nome VARCHAR(80) PRIMARY KEY,
    telefone VARCHAR(15) UNIQUE NOT NULL CHECK (telefone ~ '^[0-9]+$'),
    morada VARCHAR(255) UNIQUE NOT NULL CHECK (morada ~ '^[a-zA-Z0-9, ]+ \d{4}-\d{3} [a-zA-Z]+$')
);

CREATE TABLE enfermeiro(
    nif CHAR(9) PRIMARY KEY CHECK (nif ~ '^[0-9]+$'),
    nome VARCHAR(80) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
    morada VARCHAR(255) NOT NULL CHECK (morada ~ '^[a-zA-Z0-9, ]+ \d{4}-\d{3} [a-zA-Z]+$'),
    nome_clinica VARCHAR(80) NOT NULL REFERENCES clinica (nome)
);

CREATE TABLE medico(
    nif CHAR(9) PRIMARY KEY CHECK (nif ~ '^[0-9]+$'),
    nome VARCHAR(80) UNIQUE NOT NULL,
    telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
    morada VARCHAR(255) NOT NULL CHECK (morada ~ '^[a-zA-Z0-9, ]+ \d{4}-\d{3} [a-zA-Z]+$'),
    especialidade VARCHAR(80) NOT NULL
);

CREATE TABLE trabalha(
    nif CHAR(9) NOT NULL REFERENCES medico,
    nome VARCHAR(80) NOT NULL REFERENCES clinica,
    dia_da_semana SMALLINT CHECK (dia_da_semana BETWEEN 1 AND 7),
    PRIMARY KEY (nif, nome, dia_da_semana)
);

CREATE TABLE paciente(
    ssn CHAR(11) PRIMARY KEY CHECK (ssn ~ '^[0-9]+$'),
    nif CHAR(9) UNIQUE NOT NULL CHECK (nif ~ '^[0-9]+$'),
    nome VARCHAR(80) NOT NULL,
    telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
    morada VARCHAR(255) NOT NULL CHECK (morada ~ '^[a-zA-Z0-9, ]+ \d{4}-\d{3} [a-zA-Z]+$'),
    data_nasc DATE NOT NULL
);

CREATE TABLE consulta(
    id SERIAL PRIMARY KEY,
    ssn CHAR(11) NOT NULL REFERENCES paciente,
    nif CHAR(9) NOT NULL REFERENCES medico,
    nome VARCHAR(80) NOT NULL REFERENCES clinica,
    data DATE NOT NULL,
    hora TIME NOT NULL CHECK (hora BETWEEN '08:00' AND '12:59' OR hora BETWEEN '14:00' AND '18:59'),
    codigo_sns CHAR(12) UNIQUE CHECK (codigo_sns ~ '^[0-9]+$'),
    UNIQUE(ssn, data, hora),
    UNIQUE(nif, data, hora),
    CONSTRAINT medico_clinica_dia CHECK ((nif, nome, EXTRACT(DOW FROM data) + 1) IN (SELECT nif, nome, dia_da_semana FROM trabalha))
);

CREATE TABLE receita(
    codigo_sns VARCHAR(12) NOT NULL REFERENCES consulta (codigo_sns),
    medicamento VARCHAR(155) NOT NULL,
    quantidade SMALLINT NOT NULL CHECK (quantidade > 0),
    PRIMARY KEY (codigo_sns, medicamento)
);

CREATE TABLE observacao(
    id INTEGER NOT NULL REFERENCES consulta,
    parametro VARCHAR(155) NOT NULL,
    valor FLOAT,
    PRIMARY KEY (id, parametro)
);

-- Create additional checks and constraints
ALTER TABLE consulta ADD CONSTRAINT horario_check CHECK (
    (EXTRACT(MINUTE FROM hora) = 0 OR EXTRACT(MINUTE FROM hora) = 30)
    AND (EXTRACT(HOUR FROM hora) BETWEEN 8 AND 12 OR EXTRACT(HOUR FROM hora) BETWEEN 14 AND 18)
);
