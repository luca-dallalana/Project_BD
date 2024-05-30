SELECT 
    m.especialidade, 
    m.nome AS nome_medico, 
    c.nome AS nome_clinica, 
    o.parametro, 
    AVG(o.valor) AS media_valor, 
    STDDEV(o.valor) AS desvio_padrao_valor
FROM 
    medico m
JOIN 
    consulta co ON m.nif = co.nif
JOIN 
    clinica c ON co.nome = c.nome
JOIN 
    observacao o ON co.id = o.id
GROUP BY 
    CUBE ((m.especialidade, m.nome), c.nome, o.parametro)
ORDER BY 
    m.especialidade, 
    m.nome, 
    c.nome, 
    o.parametro;