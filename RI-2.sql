%%sql
-- RI 2 verifica se o NIF do paciente que contem SSN igual ao SSN registrado na consulta é diferente do NIF do médico que a realiza
DROP FUNCTION IF EXISTS check_doctor_patient;

CREATE OR REPLACE FUNCTION check_doctor_patient()
RETURNS TRIGGER AS
    
$$
BEGIN
    IF (SELECT p.nif 
    FROM paciente p
    WHERE p.ssn = NEW.ssn) = NEW.nif 
    THEN
        RAISE EXCEPTION 'A doctor cannot consult themselves';
    END IF;
    RETURN NEW;
END;
$$ 

LANGUAGE plpgsql;

CREATE TRIGGER check_doctor_patient_trigger
BEFORE INSERT ON consulta
FOR EACH ROW
EXECUTE FUNCTION check_doctor_patient();