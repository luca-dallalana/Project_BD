WITH soma_por_medicamento AS(
	SELECT
		medicamento, SUM(quantidade) AS quantidade
	FROM
		receita
	GROUP BY medicamento
)

SELECT
	hp.localidade, hp.nome, hp.mes, hp.dia_do_mes, m.nome, hp.especialidade, spm.medicamento, SUM(spm.quantidade)
FROM historial_paciente hp
JOIN medico m ON hp.nif = m.nif
JOIN soma_por_medicamento spm ON spm.medicamento = hp.medicamento
WHERE hp.tipo = 'receita' AND hp.ano = 2023
GROUP BY CUBE((hp.localidade, hp.nome), (hp.mes, hp.dia_do_mes), (m.nome, hp.especialidade), spm.medicamento)
