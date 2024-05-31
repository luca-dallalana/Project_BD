-- Seleciona as consultas relevantes de cardiologia, adicionando a data da consulta anterior
WITH medicamento_cardio AS (
    SELECT
        hp.ssn,
        hp.chave AS medicamento,
        hp.data,
        hp.ano,
        hp.mes,
        LAG(hp.data) OVER (PARTITION BY hp.ssn, hp.chave ORDER BY hp.data) AS prev_data
    FROM
        historial_paciente hp
    WHERE
        hp.tipo = 'receita' AND hp.especialidade = 'cardiologia'
), 
-- Calcula a diferença em meses entre a data atual e a data da consulta anterior 
-- Se a diferença for exatamente 1 mês, considera-se consecutivo 
consec_mes AS (
    SELECT
        ssn,
        medicamento,
        data,
        EXTRACT(YEAR FROM data) * 12 + EXTRACT(MONTH FROM data) AS current_month,
        EXTRACT(YEAR FROM prev_data) * 12 + EXTRACT(MONTH FROM prev_data) AS prev_month,
        CASE
            WHEN prev_data IS NULL THEN 0
            WHEN (EXTRACT(YEAR FROM data) * 12 + EXTRACT(MONTH FROM data)) -
                 (EXTRACT(YEAR FROM prev_data) * 12 + EXTRACT(MONTH FROM prev_data)) = 1 THEN 1
            ELSE 0
        END AS consecutive_flag
    FROM
        medicamento_cardio
), 
--  Cria um grupo_id que identifica sequências de meses consecutivos
grupos AS (
    SELECT
        ssn,
        medicamento,
        data,
        SUM(consecutive_flag) OVER (PARTITION BY ssn, medicamento ORDER BY data) AS grupo_id
    FROM
        consec_mes
)
SELECT
    ssn,
    medicamento,
    grupo_id
FROM
    grupos
WHERE
    grupo_id >= 12;


