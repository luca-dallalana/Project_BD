-- Indices

-- Aceleram as operações de JOIN
CREATE INDEX ssn_idx ON consulta(ssn);
CREATE INDEX id_idx ON observacao(id);

-- Um índice composto (parametro, valor) permite filtrar rapidamente as linhas que atendem a ambos os critérios
-- É mais eficiente do que usar dois índices separados para cada coluna
CREATE INDEX parametro_valor_idx ON observacao(parametro,valor);


SELECT nome
FROM paciente
JOIN consulta USING (ssn)
JOIN observacao USING (id)
WHERE parametro = ‘pressão diastólica’ AND valor >= 9;


-- Melhora no agrupamento por especialidade
CREATE INDEX especialidade_idx ON medico(especialidade);

-- Acelera a operação JOIN
CREATE INDEX nif_idx ON consulta(nif);

-- O Índice composto em data e codigo_ssn acelera a filtração baseada na data
-- O codigo_ssn acelera a operação JOIN
-- A especialidade e a qtd aceleram a seleção e as operações GROUP BY e SORT
CREATE INDEX data_ssn_esp_qtd_idx ON receita(data, codigo_ssn, especialidade, qtd);

SELECT especialidade, SUM(quantidade) AS qtd FROM medico
JOIN consulta USING (nif)
JOIN receita USING (codigo_ssn) 
WHERE data BETWEEN ‘2023-01-01’ AND ‘2023-12-31’ 
GROUP BY especialidade
SORT BY qtd;