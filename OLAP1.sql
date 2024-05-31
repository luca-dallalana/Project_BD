WITH hp_appointments_with_dates AS(
	SELECT
		hp.ssn,
		hp.chave,
		hp.valor,
		array_agg(hp.id) AS consulta_ids,
		array_agg(hp.data ORDER BY hp.data) AS consulta_dates
	FROM
		historial_paciente hp
	WHERE hp.tipo = 'observacao' AND hp.especialidade = 'ortopedia'
	GROUP BY hp.ssn, hp.chave, hp.valor, consulta_ids
)
max_intervals AS (
    SELECT
        ssn,
        parametro,
        valor,
        consulta_ids,
        consulta_dates,
        MAX(c2.data - c1.data) OVER (PARTITION BY ssn, parametro, valor) AS max_interval
    FROM
        hp_appointments_with_dates,
        LATERAL unnest(consulta_dates) WITH ORDINALITY AS c1(data, ord1),
        LATERAL unnest(consulta_dates) WITH ORDINALITY AS c2(data, ord2)
    WHERE
        ord2 > ord1
)
SELECT ssn, MAX(max_interval) as max_interval
FROM max_intervals
GROUP BY ssn
ORDER BY max_interval DESC;
