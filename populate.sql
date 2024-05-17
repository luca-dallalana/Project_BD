INSERT INTO clinica (nome, telefone, morada) VALUES
    ('Clinica A', '213456789', 'Rua A, Lisboa 1000-101'),
    ('Clinica B', '213456780', 'Rua B, Lisboa 1000-201'),
    ('Clinica C', '213456781', 'Rua C, Cascais 2750-301'),
    ('Clinica D', '213456782', 'Rua D, Sintra 2710-401'),
    ('Clinica E', '213456783', 'Rua E, Oeiras 2780-501');

-- Insert nurses
INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES
    ('100000001', 'Enfermeiro 1', '913456789', 'Rua A1, Lisboa 1000-101', 'Clinica A'),
    ('100000002', 'Enfermeiro 2', '913456780', 'Rua A2, Lisboa 1000-102', 'Clinica A'),
    ('100000003', 'Enfermeiro 3', '913456781', 'Rua A3, Lisboa 1000-103', 'Clinica A'),
    ('100000004', 'Enfermeiro 4', '913456782', 'Rua A4, Lisboa 1000-104', 'Clinica A'),
    ('100000005', 'Enfermeiro 5', '913456783', 'Rua A5, Lisboa 1000-105', 'Clinica A'),
    ('100000006', 'Enfermeiro 6', '913456784', 'Rua B1, Lisboa 1000-201', 'Clinica B'),
    ('100000007', 'Enfermeiro 7', '913456785', 'Rua B2, Lisboa 1000-202', 'Clinica B'),
    ('100000008', 'Enfermeiro 8', '913456786', 'Rua B3, Lisboa 1000-203', 'Clinica B'),
    ('100000009', 'Enfermeiro 9', '913456787', 'Rua B4, Lisboa 1000-204', 'Clinica B'),
    ('100000010', 'Enfermeiro 10', '913456788', 'Rua B5, Lisboa 1000-205', 'Clinica B'),
    ('100000011', 'Enfermeiro 11', '913456789', 'Rua C1, Cascais 2750-301', 'Clinica C'),
    ('100000012', 'Enfermeiro 12', '913456790', 'Rua C2, Cascais 2750-302', 'Clinica C'),
    ('100000013', 'Enfermeiro 13', '913456791', 'Rua C3, Cascais 2750-303', 'Clinica C'),
    ('100000014', 'Enfermeiro 14', '913456792', 'Rua C4, Cascais 2750-304', 'Clinica C'),
    ('100000015', 'Enfermeiro 15', '913456793', 'Rua C5, Cascais 2750-305', 'Clinica C'),
    ('100000016', 'Enfermeiro 16', '913456794', 'Rua D1, Sintra 2710-401', 'Clinica D'),
    ('100000017', 'Enfermeiro 17', '913456795', 'Rua D2, Sintra 2710-402', 'Clinica D'),
    ('100000018', 'Enfermeiro 18', '913456796', 'Rua D3, Sintra 2710-403', 'Clinica D'),
    ('100000019', 'Enfermeiro 19', '913456797', 'Rua D4, Sintra 2710-404', 'Clinica D'),
    ('100000020', 'Enfermeiro 20', '913456798', 'Rua D5, Sintra 2710-405', 'Clinica D'),
    ('100000021', 'Enfermeiro 21', '913456799', 'Rua E1, Oeiras 2780-501', 'Clinica E'),
    ('100000022', 'Enfermeiro 22', '913456800', 'Rua E2, Oeiras 2780-502', 'Clinica E'),
    ('100000023', 'Enfermeiro 23', '913456801', 'Rua E3, Oeiras 2780-503', 'Clinica E'),
    ('100000024', 'Enfermeiro 24', '913456802', 'Rua E4, Oeiras 2780-504', 'Clinica E'),
    ('100000025', 'Enfermeiro 25', '913456803', 'Rua E5, Oeiras 2780-505', 'Clinica E'),
    ('100000026', 'Enfermeiro 26', '913456804', 'Rua E6, Oeiras 2780-506', 'Clinica E');

-- Insert doctors
INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES
    ('200000001', 'Medico 1', '923456789', 'Rua A1, Lisboa 1000-101', 'clinica geral'),
    ('200000002', 'Medico 2', '923456780', 'Rua A2, Lisboa 1000-102', 'clinica geral'),
    ('200000003', 'Medico 3', '923456781', 'Rua A3, Lisboa 1000-103', 'clinica geral'),
    ('200000004', 'Medico 4', '923456782', 'Rua A4, Lisboa 1000-104', 'clinica geral'),
    ('200000005', 'Medico 5', '923456783', 'Rua A5, Lisboa 1000-105', 'clinica geral'),
    ('200000006', 'Medico 6', '923456784', 'Rua B1, Lisboa 1000-201', 'clinica geral'),
    ('200000007', 'Medico 7', '923456785', 'Rua B2, Lisboa 1000-202', 'clinica geral'),
    ('200000008', 'Medico 8', '923456786', 'Rua B3, Lisboa 1000-203', 'clinica geral'),
    ('200000009', 'Medico 9', '923456787', 'Rua B4, Lisboa 1000-204', 'clinica geral'),
    ('200000010', 'Medico 10', '923456788', 'Rua B5, Lisboa 1000-205', 'clinica geral'),
    ('200000011', 'Medico 11', '923456789', 'Rua C1, Cascais 2750-301', 'clinica geral'),
    ('200000012', 'Medico 12', '923456790', 'Rua C2, Cascais 2750-302', 'clinica geral'),
    ('200000013', 'Medico 13', '923456791', 'Rua C3, Cascais 2750-303', 'clinica geral'),
    ('200000014', 'Medico 14', '923456792', 'Rua C4, Cascais 2750-304', 'clinica geral'),
    ('200000015', 'Medico 15', '923456793', 'Rua C5, Cascais 2750-305', 'clinica geral'),
    ('200000016', 'Medico 16', '923456794', 'Rua D1, Sintra 2710-401', 'clinica geral'),
    ('200000017', 'Medico 17', '923456795', 'Rua D2, Sintra 2710-402', 'clinica geral'),
    ('200000018', 'Medico 18', '923456796', 'Rua D3, Sintra 2710-403', 'clinica geral'),
    ('200000019', 'Medico 19', '923456797', 'Rua D4, Sintra 2710-404', 'clinica geral'),
    ('200000020', 'Medico 20', '923456798', 'Rua D5, Sintra 2710-405', 'clinica geral'),
    ('200000021', 'Medico 21', '923456799', 'Rua E1, Oeiras 2780-501', 'ortopedia'),
    ('200000022', 'Medico 22', '923456800', 'Rua E2, Oeiras 2780-502', 'ortopedia'),
    ('200000023', 'Medico 23', '923456801', 'Rua E3, Oeiras 2780-503', 'ortopedia'),
    ('200000024', 'Medico 24', '923456802', 'Rua E4, Oeiras 2780-504', 'ortopedia'),
    ('200000025', 'Medico 25', '923456803', 'Rua E5, Oeiras 2780-505', 'ortopedia'),
    ('200000026', 'Medico 26', '923456804', 'Rua A1, Lisboa 1000-101', 'cardiologia'),
    ('200000027', 'Medico 27', '923456805', 'Rua A2, Lisboa 1000-102', 'cardiologia'),
    ('200000028', 'Medico 28', '923456806', 'Rua A3, Lisboa 1000-103', 'cardiologia'),
    ('200000029', 'Medico 29', '923456807', 'Rua A4, Lisboa 1000-104', 'cardiologia'),
    ('200000030', 'Medico 30', '923456808', 'Rua A5, Lisboa 1000-105', 'cardiologia'),
    ('200000031', 'Medico 31', '923456809', 'Rua B1, Lisboa 1000-201', 'dermatologia'),
    ('200000032', 'Medico 32', '923456810', 'Rua B2, Lisboa 1000-202', 'dermatologia'),
    ('200000033', 'Medico 33', '923456811', 'Rua B3, Lisboa 1000-203', 'dermatologia'),
    ('200000034', 'Medico 34', '923456812', 'Rua B4, Lisboa 1000-204', 'dermatologia'),
    ('200000035', 'Medico 35', '923456813', 'Rua B5, Lisboa 1000-205', 'dermatologia'),
    ('200000036', 'Medico 36', '923456814', 'Rua C1, Cascais 2750-301', 'neurologia'),
    ('200000037', 'Medico 37', '923456815', 'Rua C2, Cascais 2750-302', 'neurologia'),
    ('200000038', 'Medico 38', '923456816', 'Rua C3, Cascais 2750-303', 'neurologia'),
    ('200000039', 'Medico 39', '923456817', 'Rua C4, Cascais 2750-304', 'neurologia'),
    ('200000040', 'Medico 40', '923456818', 'Rua C5, Cascais 2750-305', 'neurologia'),
    ('200000041', 'Medico 41', '923456819', 'Rua D1, Sintra 2710-401', 'pediatria'),
    ('200000042', 'Medico 42', '923456820', 'Rua D2, Sintra 2710-402', 'pediatria'),
    ('200000043', 'Medico 43', '923456821', 'Rua D3, Sintra 2710-403', 'pediatria'),
    ('200000044', 'Medico 44', '923456822', 'Rua D4, Sintra 2710-404', 'pediatria'),
    ('200000045', 'Medico 45', '923456823', 'Rua D5, Sintra 2710-405', 'pediatria'),
    ('200000046', 'Medico 46', '923456824', 'Rua E1, Oeiras 2780-501', 'pediatria'),
    ('200000047', 'Medico 47', '923456825', 'Rua E2, Oeiras 2780-502', 'pediatria'),
    ('200000048', 'Medico 48', '923456826', 'Rua E3, Oeiras 2780-503', 'pediatria'),
    ('200000049', 'Medico 49', '923456827', 'Rua E4, Oeiras 2780-504', 'pediatria'),
    ('200000050', 'Medico 50', '923456828', 'Rua E5, Oeiras 2780-505', 'pediatria'),
    ('200000051', 'Medico 51', '923456829', 'Rua A1, Lisboa 1000-101', 'ortopedia'),
    ('200000052', 'Medico 52', '923456830', 'Rua A2, Lisboa 1000-102', 'ortopedia'),
    ('200000053', 'Medico 53', '923456831', 'Rua A3, Lisboa 1000-103', 'ortopedia'),
    ('200000054', 'Medico 54', '923456832', 'Rua A4, Lisboa 1000-104', 'ortopedia'),
    ('200000055', 'Medico 55', '923456833', 'Rua A5, Lisboa 1000-105', 'ortopedia'),
    ('200000056', 'Medico 56', '923456834', 'Rua B1, Lisboa 1000-201', 'cardiologia'),
    ('200000057', 'Medico 57', '923456835', 'Rua B2, Lisboa 1000-202', 'cardiologia'),
    ('200000058', 'Medico 58', '923456836', 'Rua B3, Lisboa 1000-203', 'cardiologia'),
    ('200000059', 'Medico 59', '923456837', 'Rua B4, Lisboa 1000-204', 'cardiologia'),
    ('200000060', 'Medico 60', '923456838', 'Rua B5, Lisboa 1000-205', 'cardiologia');

-- Assign doctors to clinics
DO $$
DECLARE
    doctor RECORD;
    clinic RECORD;
    dow SMALLINT;
BEGIN
    FOR doctor IN (SELECT nif FROM medico) LOOP
        FOR clinic IN (SELECT nome FROM clinica ORDER BY random() LIMIT 2) LOOP
            FOR dow IN 1..7 LOOP
                INSERT INTO trabalha (nif, nome, dia_da_semana)
                VALUES (doctor.nif, clinic.nome, dow);
            END LOOP;
        END LOOP;
    END LOOP;
END $$;

-- Insert patients
DO $$
DECLARE
    i INTEGER;
    ssn CHAR(11);
    nif CHAR(9);
    name VARCHAR(80);
    phone VARCHAR(15);
    address VARCHAR(255);
BEGIN
    FOR i IN 1..5000 LOOP
        ssn := LPAD(i::TEXT, 11, '0');
        nif := LPAD(i::TEXT, 9, '0');
        name := 'Paciente ' || i;
        phone := '9123456' || LPAD((i % 100)::TEXT, 2, '0');
        address := 'Rua ' || i || ', Lisboa 1000-' || LPAD(i::TEXT, 3, '0');
        INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES (ssn, nif, name, phone, address, '1990-01-01');
    END LOOP;
END $$;

-- Insert consultations
DO $$
DECLARE
    i INTEGER;
    patient_ssn CHAR(11);
    doctor_nif CHAR(9);
    clinic_name VARCHAR(80);
    consult_date DATE;
    consult_time TIME;
    sns_code CHAR(12);
BEGIN
    FOR i IN 1..5000 LOOP
        patient_ssn := LPAD(i::TEXT, 11, '0');
        doctor_nif := (SELECT nif FROM medico ORDER BY random() LIMIT 1);
        clinic_name := (SELECT nome FROM clinica ORDER BY random() LIMIT 1);
        consult_date := '2023-01-01'::DATE + (i % 730);
        consult_time := ('08:00'::TIME + (i % 20) * '00:30'::INTERVAL);
        sns_code := LPAD(i::TEXT, 12, '0');
        INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES (patient_ssn, doctor_nif, clinic_name, consult_date, consult_time, sns_code);
    END LOOP;
END $$;

-- Insert prescriptions
DO $$
DECLARE
    consult_id INTEGER;
    med_code CHAR(12);
    drug VARCHAR(155);
    qty SMALLINT;
BEGIN
    FOR consult_id IN (SELECT id FROM consulta) LOOP
        IF random() < 0.8 THEN
            med_code := (SELECT codigo_sns FROM consulta WHERE id = consult_id);
            FOR qty IN 1..(1 + (random() * 5)::INTEGER) LOOP
                drug := 'Medicamento ' || qty;
                INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES (med_code, drug, 1 + (random() * 2)::SMALLINT);
            END LOOP;
        END IF;
    END LOOP;
END $$;

-- Insert observations
DO $$
DECLARE
    consult_id INTEGER;
    param VARCHAR(155);
    value FLOAT;
BEGIN
    FOR consult_id IN (SELECT id FROM consulta) LOOP
        FOR param IN (SELECT 'Sintoma ' || g FROM generate_series(1, 50) AS g) LOOP
            IF random() < 0.1 THEN
                INSERT INTO observacao (id, parametro) VALUES (consult_id, param);
            END IF;
        END LOOP;
        FOR param IN (SELECT 'Metrica ' || g FROM generate_series(1, 20) AS g) LOOP
            IF random() < 0.1 THEN
                value := random() * 100;
                INSERT INTO observacao (id, parametro, valor) VALUES (consult_id, param, value);
            END IF;
        END LOOP;
    END LOOP;
END $$;