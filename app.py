##!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig
from datetime import datetime, time
import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.

# Mudei para a DB que ta no report
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

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

def is_valid_date(date_string):
    try:
        # Try to create a datetime object from the string
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        # If the string cannot be parsed, it's an invalid date
        return False

def is_valid_time(time_str):
    try:
        t = datetime.strptime(time_str, '%H:%M').time()
        if t.minute not in (0, 30):
            return False
        if (t >= time(8, 0) and t <= time(12, 30)) or (t >= time(15, 0) and t <= time(18, 30)):
            return True
        return False
    except ValueError:
        return False

@app.route("/", methods=("GET",))
def clinica():
    """Show all the clinics names and adresses."""
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                clinicas = cur.execute(
                    """
                    SELECT c.nome, c.morada
                    FROM clinica c
                    ORDER BY c.nome, c.morada;
                    """,                    
                ).fetchall()
                log.debug(f"Found {cur.rowcount} clinicas.")
                if cur.rowcount == 0:
                    return jsonify({"message": "Clinics not found.", "status": "error"}), 404
                return jsonify(clinicas), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 500


@app.route("/c/<clinica>/", methods=("GET",))
def especialidades_clinica(clinica):
    """Show all the medical specialties of the given clinic."""

    if not clinica:
        return jsonify({"message": "Invalid arguments", "status": "error"}), 400
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.nome
                    FROM clinica c
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"clinica": clinica},
                ).fetchall
                if cur.rowcount == 0:
                    return jsonify({"message": "Clinics not found.", "status": "error"}), 404
                especialidades_clinicas = cur.execute(
                    """
                    SELECT m.especialidade
                    FROM medico m
                    JOIN trabalha t ON t.nif = m.nif
                    JOIN clinica c ON c.nome = t.nome
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"clinica": clinica},
                ).fetchall()
                if cur.rowcount == 0:
                    return jsonify({"message": "Specialties not found.", "status": "error"}), 404
                log.debug(f"Found {cur.rowcount} especialidades em {clinica}.")
                return jsonify(especialidades_clinicas), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 500

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def consultas_livres(clinica, especialidade):
    """Show all the doctors of the chosen specialty that work at the specific 
    clinic and lists their first three free appointment times."""

    if not clinica or not especialidade:
        return jsonify({"message": "Invalid arguments", "status": "error"}), 400

    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    
                    """,
                    {"clinica": clinica, "especialidade": especialidade},
                ).fetchall()
                log.debug(f"Found {cur.rowcount} especialidades em {clinica}.")
                return jsonify()
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 500

@app.route("/a/<clinica>/registar/", methods=("POST",))
def registra_consulta(clinica):
    """Marca uma consulta"""

    paciente_ssn = request.args.get('paciente.ssn')
    medico_nif = request.args.get('medico.nif')
    data = request.args.get('data.data')
    time = request.args.get('data.hora')

    if not paciente_ssn or not medico_nif or not data or not time:
        return jsonify({"message": "Invalid arguments", "status": "error"}), 400
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.nome
                    FROM clinica c
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"clinica": clinica},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Clinic not found.", "status": "error"}), 404
                
                cur.execute(
                    """
                    SELECT p.ssn
                    FROM paciente p
                    WHERE p.ssn = %(paciente_ssn)s;
                    """,
                    {"paciente_ssn": paciente_ssn},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Pacient not found.", "status": "error"}), 404
                
                cur.execute(
                    """
                    SELECT m.nif
                    FROM medico m
                    WHERE m.nif = %(medico_nif)s;
                    """,
                    {"medico_nif": medico_nif},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Doctor not found.", "status": "error"}), 404
                
                if not is_valid_date(data):
                    return jsonify({"message": "Invalid Date.", "status": "error"}), 400
                
                if not is_valid_time(time):
                    return jsonify({"message": "Invalid Time.", "status": "error"}), 400
                
                data_hora = datetime.combine(data, time)
                if data_hora <= datetime.now():
                    return jsonify({"message": "The provided date and time must be in the future", "status": "error"}), 400
                
                # Verificar se o médico trabalha na clínica nesse dia
                cur.execute(
                """
                SELECT 1 
                FROM trabalha t
                WHERE t.nif = %(medico_nif)s AND t.nome = %(clinica)s AND t.dia_da_semana = EXTRACT(DOW FROM %(data)s);
                """, 
                {"medico_nif": medico_nif, "clinica": clinica, "data": data}
                )
                if not cur.fetchone():
                    return jsonify({"message": "Doctor doesnt work in the clinic this day.", "status": "error"}), 400

                # Verificar se ja existe uma consulta marcada
                cur.execute(
                    """
                    SELECT 1 
                    FROM consulta c
                    WHERE c.ssn = %(paciente_ssn)s AND c.nif = %(medico_nif)s AND 
                    c.nome = %(clinica)s AND c.data = %(data)s AND c.time = %(time)s;
                    """,
                    {"paciente_ssn": paciente_ssn, "medico_nif": medico_nif, "clinica": clinica, "data":data, "time": time}
                )
                if cur.fetchone():
                    return jsonify({"message": "This appointment already exists.", "status": "error"}), 400
                    
                with conn.transaction():
                    # Registrar a consulta
                    cur.execute(
                        """
                        INSERT INTO consulta (ssn, nif, nome, data, hora)
                        VALUES (%(paciente_ssn)s, %(medico_nif)s, %(clinica)s, %(data)s, %(time)s);
                        """, 
                        {"paciente_ssn": paciente_ssn, "medico_nif": medico_nif, "clinica": clinica, "data":data, "time": time}
                    )
                    conn.commit()
                    return jsonify({"message": "Consulta registrada com sucesso", "status": "success"}), 201
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 500


@app.route("/a/<clinica>/cancelar/", methods=("DELETE","POST",))
def desmarca_consulta(clinica):
    """Desmarca uma consulta."""

    paciente_ssn = request.args.get('paciente.ssn')
    medico_nif = request.args.get('medico.nif')
    data = request.args.get('data.data')
    time = request.args.get('data.hora')

    if not paciente_ssn or not medico_nif or not data or not time:
        return jsonify({"message": "Invalid arguments", "status": "error"}), 400
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.nome
                    FROM clinica c
                    WHERE c.nome = %(clinica)s;
                    """,
                    {"clinica": clinica},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Clinic not found.", "status": "error"}), 404
                
                cur.execute(
                    """
                    SELECT p.ssn
                    FROM paciente p
                    WHERE p.ssn = %(paciente_ssn)s;
                    """,
                    {"paciente_ssn": paciente_ssn},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Pacient not found.", "status": "error"}), 404
                
                cur.execute(
                    """
                    SELECT m.nif
                    FROM medico m
                    WHERE m.nif = %(medico_nif)s;
                    """,
                    {"medico_nif": medico_nif},
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Doctor not found.", "status": "error"}), 404
                
                if not is_valid_date(data):
                    return jsonify({"message": "Invalid Date.", "status": "error"}), 400
                
                if not is_valid_time(time):
                    return jsonify({"message": "Invalid Time.", "status": "error"}), 400
                
                data_hora = datetime.combine(data, time)
                if data_hora <= datetime.now():
                    return jsonify({"message": "The provided date and time must be in the future", "status": "error"}), 400
                
                # Verificar se o médico trabalha na clínica nesse dia
                cur.execute(
                """
                SELECT 1 
                FROM trabalha t
                WHERE t.nif = %(medico_nif)s AND t.nome = %(clinica)s AND t.dia_da_semana = EXTRACT(DOW FROM %(data)s);
                """, 
                {"medico_nif": medico_nif, "clinica": clinica, "data": data}
                )
                if not cur.fetchone():
                    return jsonify({"message": "Doctor doesnt work in the clinic this day.", "status": "error"}), 400
                
                with conn.transaction():
                    cur.execute(
                        """
                        DELETE FROM consulta c
                        WHERE c.ssn = %(paciente_ssn)s AND c.nif = %(medico_nif)s AND 
                        c.nome = %(clinica)s AND c.data = %(data)s AND c.time = %(time)s;
                        """,
                        {"paciente_ssn": paciente_ssn, "medico_nif": medico_nif, "clinica": clinica, "data":data, "time": time}
                    )
                    if cur.rowcount == 0:
                        return jsonify({"message": "Appointment not found.", "status": "error"}), 404

                    conn.commit()
                    return jsonify({"message": "Appointment deleted.", "status": "success"}), 200
    except Exception as e:
        return jsonify({"Internal Server Error": str(e)}), 500
    
if __name__ == "__main__":
    app.run()