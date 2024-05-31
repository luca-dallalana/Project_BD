SELECT 
    hp.especialidade, 
    hp.nome AS nome_medico, 
    hp.nome AS nome_clinica, 
    hp.chave, 
    AVG(hp.valor) AS media_valor, 
    STDDEV(hp.valor) AS desvio_padrao_valor
FROM 
    historial_paciente hp
WHERE hp.tipo = 'observacao'
GROUP BY 
    CUBE ((hp.especialidade, hp.nome), hp.nome, hp.chave)
ORDER BY 
    hp.especialidade, 
    hp.nome, 
    hp.nome, 
    hp.chave;