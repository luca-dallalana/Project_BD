%%sql
-- RI 3 verifica se o médico da consulta esta registrado para trabalhar naquela data
DROP FUNCTION IF EXISTS check_doctor_schedule;

CREATE OR REPLACE FUNCTION check_doctor_schedule()
RETURNS TRIGGER AS 
    
$$
DECLARE
    dia_semana SMALLINT;
BEGIN
    dia_semana := EXTRACT(DOW FROM NEW.data);
    IF dia_semana = 0 THEN
        dia_semana := 7;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM trabalha t
        WHERE t.nif = NEW.nif
        AND t.nome = NEW.nome
        AND t.dia_da_semana = dia_semana
    ) 
    THEN
        RAISE EXCEPTION 'Doctor does not work at the clinic on the specified day';
    END IF;

    RETURN NEW;
END;
$$ 

LANGUAGE plpgsql;

CREATE TRIGGER check_doctor_schedule_trigger
BEFORE INSERT ON consulta
FOR EACH ROW
EXECUTE FUNCTION check_doctor_schedule();