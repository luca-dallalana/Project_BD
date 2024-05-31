%%sql
DROP MATERIALIZED VIEW IF EXISTS historial_paciente;

CREATE MATERIALIZED VIEW historial_paciente AS
SELECT
    c.id, 
    c.ssn, 
    c.nif, 
    c.nome, 
    c.data,
    EXTRACT(YEAR FROM c.data) AS ano,
    EXTRACT(MONTH FROM c.data) AS mes,
    EXTRACT(DAY FROM c.data) AS dia_do_mes,
    SUBSTRING(cl.morada FROM POSITION(', ' IN cl.morada) + 2) AS localidade, 
    m.especialidade,
    'observacao' AS tipo,
    o.parametro AS chave,
    o.valor AS valor
FROM 
    consulta c
JOIN 
    paciente p ON c.ssn = p.ssn
JOIN 
    clinica cl ON c.nome = cl.nome
JOIN 
    medico m ON c.nif = m.nif
LEFT JOIN 
    observacao o ON c.id = o.id

UNION ALL

SELECT
    c.id, 
    c.ssn, 
    c.nif, 
    c.nome, 
    c.data,
    EXTRACT(YEAR FROM c.data) AS ano,
    EXTRACT(MONTH FROM c.data) AS mes,
    EXTRACT(DAY FROM c.data) AS dia_do_mes,
    SUBSTRING(cl.morada FROM POSITION(', ' IN cl.morada) + 2) AS localidade, 
    m.especialidade,
    'receita' AS tipo,
    r.medicamento AS chave,
    r.quantidade AS valor
FROM 
    consulta c
JOIN 
    paciente p ON c.ssn = p.ssn
JOIN 
    clinica cl ON c.nome = cl.nome
JOIN 
    medico m ON c.nif = m.nif
LEFT JOIN 
    receita r ON c.codigo_sns = r.codigo_sns;
