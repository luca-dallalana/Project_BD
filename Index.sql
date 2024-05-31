-- Indices

%%sql
-- CREATE INDEX ...
-- Aceleram as operações de JOIN
%%sql
-- CREATE INDEX ...
-- Aceleram as operações de JOIN
DROP INDEX IF EXISTS idx_paciente_consulta_ssn;
CREATE INDEX idx_paciente_consulta_ssn ON  consulta(ssn);

DROP INDEX IF EXISTS idx_consulta_observacao_id;
CREATE INDEX idx_consulta_observacao_id ON  observacao(id);

-- Um índice composto (parametro, valor) permite filtrar rapidamente as linhas que atendem a ambos os critérios
-- É mais eficiente do que usar dois índices separados para cada coluna
DROP INDEX IF EXISTS parametro_valor_idx;
CREATE INDEX parametro_valor_idx ON observacao(parametro,valor);


-- CREATE INDEX ...

-- A especialidade e a qtd aceleram a seleção e as operações GROUP BY e SORT
%%sql
-- CREATE INDEX ...
-- A especialidade e a qtd aceleram a seleção e as operações GROUP BY e SORT
DROP INDEX IF EXISTS idx_medico_especialidade;
CREATE INDEX idx_medico_especialidade ON medico(especialidade);

DROP INDEX IF EXISTS idx_receita_sns;
CREATE INDEX idx_receita_sns ON receita(codigo_sns);

DROP INDEX IF EXISTS idx_receita_quantidade;
CREATE INDEX idx_receita_quantidade ON receita(quantidade);

DROP INDEX IF EXISTS idx_consulta_data;
CREATE INDEX idx_consulta_data ON consulta(data);
