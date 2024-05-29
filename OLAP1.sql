WITH orthopedic_appointments AS (
    SELECT
        c.ssn,
        c.id AS consulta_id,
        o.parametro,
        o.valor
    FROM
        consulta c
    JOIN medico m ON c.nif = m.nif
    JOIN observacao o ON c.id = o.id
    WHERE
        m.especialidade = 'ortopedia'
),
grouped_appointments AS (
    SELECT
        ssn,
        parametro,
        valor,
        array_agg(consulta_id) AS consulta_ids
    FROM
        orthopedic_appointments
    GROUP BY
        ssn, parametro, valor
),
appointments_with_dates AS (
    SELECT
        ga.ssn,
        ga.parametro,
        ga.valor,
        ga.consulta_ids,
        array_agg(c.data ORDER BY c.data) AS consulta_dates
    FROM
        grouped_appointments ga
    JOIN consulta c ON c.id = ANY(ga.consulta_ids)
    GROUP BY
        ga.ssn, ga.parametro, ga.valor, ga.consulta_ids
),
max_intervals AS (
    SELECT
        ssn,
        parametro,
        valor,
        consulta_ids,
        consulta_dates,
        MAX(c2.data - c1.data) OVER (PARTITION BY ssn, parametro, valor) AS max_interval
    FROM
        appointments_with_dates,
        LATERAL unnest(consulta_dates) WITH ORDINALITY AS c1(data, ord1),
        LATERAL unnest(consulta_dates) WITH ORDINALITY AS c2(data, ord2)
    WHERE
        ord2 > ord1
)
SELECT ssn, MAX(max_interval) as max_interval
FROM max_intervals
GROUP BY ssn
ORDER BY max_interval DESC;
