SELECT 
    COALESCE(especialidade, 'total') AS nivel,
    CASE 
        WHEN GROUPING(especialidade) = 1 THEN NULL
        ELSE AVG(valor) 
    END AS media,
    CASE 
        WHEN GROUPING(especialidade) = 1 THEN NULL
        ELSE STDDEV(valor) 
    END AS desvio_padrao
FROM historial_paciente
GROUP BY GROUPING SETS (
    (),
    (especialidade),
    (especialidade, m.nome),
    (especialidade, m.nome, cl.nome)
);
