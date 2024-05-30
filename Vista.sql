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
    CASE 
        WHEN o.parametro IS NOT NULL THEN 'observacao'
        WHEN r.medicamento IS NOT NULL THEN 'receita'
    END AS tipo,
    COALESCE(o.parametro, r.medicamento) AS chave,
    COALESCE(o.valor, r.quantidade) AS valor
FROM 
    consulta c
JOIN 
    clinica cl ON c.nome = cl.nome
JOIN 
    medico m ON c.nif = m.nif
LEFT JOIN 
    observacao o ON c.id = o.id
LEFT JOIN 
    receita r ON c.codigo_sns = r.codigo_sns;
