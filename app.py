#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.

# Mudei para a DB que ta no report
DATABASE_URL = os.environ.get("DATABASE_URL", "saude:saude@postgres/saude")

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger

@app.route("/", methods=("GET",))
def clinica():
    """Show all the clinics names and adresses."""
    try:
        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                clinicas = cur.execute(
                    """
                    SELECT c.nome, c.morada
                    FROM clinica c
                    ORDER BY c.nome, c.morada;
                    """,
                    {},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} clinicas.")
                return jsonify(clinicas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/c/<clinica>/", methods=("GET",))
def especialidades_clinica(clinica):
    """Show all the medical specialties of the given clinic."""
    try:
        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                especialidades_clinicas = cur.execute(
                    """
                    SELECT m.especialidade
                    FROM medico m
                    JOIN trabalha t ON t.nif = m.nif
                    JOIN clinica c ON c.nome = t.nome
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"nome": clinica},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} especialidades em {clinica}.")
                return jsonify(especialidades_clinicas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def consultas_livres(clinica, especialidade):
    """Show all the doctors of the chosen specialty that work at the specific 
    clinic and lists their first three free appointment times."""
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                
                """,
                {"clinica": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} especialidades em {clinica}.")
    return jsonify()


@app.route("//a/<clinica>/registar/", methods=("POST",))
def registra_consulta(clinica):
    """Marca uma consulta"""
    data = request.get_json()

    paciente_ssn = data.get('paciente.ssn')
    medico_nif = data.get('medico.nif')
    data_hora = data.get('data.hora')

    if not paciente_ssn or not medico_nif or not data_hora:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                # Verificar se o médico trabalha na clínica nesse dia
                cur.execute("""
                    SELECT 1 FROM trabalha
                    WHERE nif = %s AND nome = %s AND dia_da_semana = EXTRACT(DOW FROM %s);
                """, (medico_nif, clinica, data_hora))
                if not cur.fetchone():
                    return jsonify({"error": "Medico não trabalha na clinica nesse dia"}), 400

                # Registrar a consulta
                cur.execute("""
                    INSERT INTO consulta (ssn, nif, nome, data, hora)
                    VALUES (%s, %s, %s, %s, %s);
                """, (paciente_ssn, medico_nif, clinica, data_hora.date(), data_hora.time()))
                conn.commit()
                return jsonify({"message": "Consulta registrada com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/a/<clinica>/cancelar/", methods=("DELETE","POST",))
def desmarca_consulta(clinica):
    """Desmarca uma consulta."""
    try:
        data = request.get_json()
        paciente_ssn = data.get('paciente.ssn')
        medico_nif = data.get('medico.nif')
        data_consulta = data['data']
        hora_consulta = data['hora']

        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM consulta c
                    WHERE c.ssn = %s AND c.nif = %s AND c.nome = %s 
                    AND (data > %s OR (data = %s AND hora > %s));
                """, (paciente_ssn, medico_nif, clinica, data_consulta, data_consulta, hora_consulta))
                if cur.rowcount == 0:
                    return jsonify({"error": "Consulta não encontrada ou já ocorreu."}), 404

                conn.commit()
                return jsonify({"message": "Consulta cancelada com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run()