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


@app.route("/c/<clinica>/", methods=("GET",))
def especialidades_clinica(clinica):
    """Show all the medical specialties of the given clinic."""

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
            )
    return jsonify()


@app.route("//a/<clinica>/registar/", methods=("POST",))
def registra_consulta(clinica):
    """Marca uma consulta"""
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                
                """,
            )
        conn.commit()
    return "", 204


@app.route("/a/<clinica>/cancelar/", methods=("DELETE","POST",))
def desmarca_consulta(clinica):
    """Desmarca uma consulta."""

    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """

                """,
                {"account_number": clinica},
            )
        conn.commit()
    return "", 204

if __name__ == "__main__":
    app.run()