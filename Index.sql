-- Indices

%%sql
-- CREATE INDEX ...
-- Aceleram as operações de JOIN
CREATE INDEX idx_paciente_consulta_ssn ON paciente(ssn), consulta(ssn);
CREATE INDEX idx_consulta_observacao_id ON consulta(id), observacao(id);

-- Um índice composto (parametro, valor) permite filtrar rapidamente as linhas que atendem a ambos os critérios
-- É mais eficiente do que usar dois índices separados para cada coluna
CREATE INDEX parametro_valor_idx ON observacao(parametro,valor);


SELECT nome
FROM paciente
JOIN consulta USING (ssn)
JOIN observacao USING (id)
WHERE parametro = 'pressão diastólica' AND valor >= 9;


-- CREATE INDEX ...

-- Acelera a operação JOIN
CREATE INDEX idx_medico_consulta_nif ON medico(nif), consulta(nif);
CREATE INDEX idx_consulta_receita_codigo_sns ON consulta(codigo_sns), receita(codigo_sns);

-- A especialidade e a qtd aceleram a seleção e as operações GROUP BY e SORT
CREATE INDEX idx_medico_especialidade ON medico(especialidade);
CREATE INDEX idx_consulta_data ON consulta(data);

SELECT especialidade, SUM(quantidade) AS qtd FROM medico
JOIN consulta USING (nif)
JOIN receita USING (codigo_ssn) 
WHERE data BETWEEN ‘2023-01-01’ AND ‘2023-12-31’ 
GROUP BY especialidade
SORT BY qtd;