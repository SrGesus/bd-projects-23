from psycopg.rows import namedtuple_row
import os
from logging.config import dictConfig
import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
import re

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger

# DATABASE_URL environment variable if it exists, otherwise use this.
# Format postgres://username:password@hostname/database_name.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres/postgres")

@app.route("/", methods=("GET",))
@app.route("/c/", methods=("GET",))
def clinic_index(): 

    query = """
    SELECT nome, morada FROM clinica;
    """   
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            clinics = cur.execute(query, ()).fetchall() 
            log.debug(f"Found {cur.rowcount} rows.")
    
    return jsonify(clinics)


@app.route("/c/<clinica>/", methods=("GET",))
def especialidade_index(clinica):
    """Lista todas as especialidades oferecidas na clínica especificada."""
    
    query = """
    SELECT DISTINCT especialidade 
    FROM trabalha t 
    JOIN medico m USING(nif) 
    WHERE t.nome = %s
    """
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(query, (clinica,))
            especialidades = cur.fetchall()
            log.debug(f"Found {cur.rowcount} rows for clinic {clinica}.")
    
    return jsonify([especialidade.especialidade for especialidade in especialidades])


@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def medic_index(clinica, especialidade):
   
    query_medicos = """
    SELECT DISTINCT m.nome, nif
    FROM trabalha t 
    JOIN medico m USING(nif)
    WHERE t.nome = %s AND m.especialidade = %s;

    """
    
    query_horarios = """
    WITH RECURSIVE time_range AS (
        SELECT CURRENT_DATE::date AS data, hora
        FROM distinct_horas
        UNION ALL
        SELECT (data + INTERVAL '1 day')::date, hora
        FROM time_range
    )
    SELECT data, hora 
    FROM time_range AS t
    WHERE (data > CURRENT_DATE OR hora > CURRENT_TIMESTAMP::time) AND
    EXTRACT(ISODOW FROM data) IN (
        SELECT dia_da_semana
        FROM trabalha
        WHERE nif = %(nif)s AND nome = %(clinica)s
    ) AND NOT EXISTS (
        SELECT 1 FROM consulta c
        WHERE c.nif = %(nif)s AND c.data = t.data AND c.hora = t.hora
    )
    LIMIT 3;
    """
    result = {}
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            # Buscar médicos
            cur.execute(query_medicos, (clinica, especialidade))
            medicos = cur.fetchall()
            log.debug(f"Found {cur.rowcount} medicos for clinic {clinica} and specialty {especialidade}.")
            
            for medico in medicos:
                # Buscar horários para cada médico
                cur.execute(query_horarios, {
                    "nif": medico.nif, "clinica": clinica,
                })
                horarios = cur.fetchall()
                result[medico.nome] = [(horario.data.strftime('%Y-%m-%d'), horario.hora.strftime('%H:%M:%S')) for horario in horarios]
    
    return jsonify(result)


@app.route("/a/<clinica>/", methods=("GET",))
def consultas_get(clinica):
    """Lista próximas consultas marcadas na clínica especificada."""

    query = """
    SELECT c.ssn, c.nif, c.data, c.hora
    FROM consulta c
    WHERE c.nome = %s 
    AND (c.data > CURRENT_DATE)
    OR (c.data = CURRENT_DATE AND c.hora >= CURRENT_TIMESTAMP::time)
    ORDER BY c.data, c.hora
    LIMIT 20;
    """

    results = []
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(query, (clinica,))
            consultas = cur.fetchall()
            log.debug(f"Found {cur.rowcount} rows for clinic {clinica}.")
            for consulta in consultas:
                results.append({
                    "paciente": consulta.ssn,
                    "medico": consulta.nif,
                    "data": consulta.data.strftime('%Y-%m-%d'),
                    "hora": consulta.hora.strftime('%H:%M:%S'),
                })
    return jsonify(results)


@app.route("/a/<clinica>/registar/", methods=("POST",))
def consultas_regista(clinica):
    # Receber os dados da requisição
    paciente = request.json.get('paciente')
    medico = request.json.get('medico')
    data = request.json.get('data')  
    hora = request.json.get('hora')  

    if not paciente:
        return jsonify({"error": "Parâmetro paciente em falta"}), 400
    if not medico:
        return jsonify({"error": "Parâmetro medico em falta"}), 400
    if not data:
        return jsonify({"error": "Parâmetro data em falta"}), 400
    if data and not re.match(r"\d{4}-\d{2}-\d{2}", data):
        return jsonify({"error": "Formato de data inválido"}), 400
    if not hora:
        return jsonify({"error": "Parâmetro hora em falta"}), 400
    if hora and not re.match(r"\d{2}:\d{2}:\d{2}", hora):
        return jsonify({"error": "Formato de hora inválido"}), 400
    
    verifica_data_query = """SELECT 1 
    FROM distinct_horas 
    WHERE (
    (hora > CURRENT_TIMESTAMP::time AND %(data)s=CURRENT_DATE) 
    OR %(data)s>CURRENT_DATE
    ) AND (hora = %(hora)s);
    """

    verifica_paciente_query = """
    SELECT ssn FROM paciente 
    WHERE ssn = %s;
    """

    verifica_medico_query = """
    SELECT nif FROM medico
    WHERE nome = %s;
    """

    regista_query = """
    INSERT INTO consulta (ssn, nif, nome, data, hora) VALUES(%s, %s, %s, %s, %s);
    """

    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(verifica_paciente_query, (paciente,))
            if cur.rowcount == 0:
                return jsonify({"error": "Paciente não está registado."}), 404
            cur.fetchall()
            cur.execute(verifica_medico_query, (medico,))
            if cur.rowcount == 0:
                return jsonify({"error": "Médico não encontrado."}), 404
            nif = cur.fetchone().nif
            cur.execute(verifica_data_query, {
                    "data": data, "hora": hora,
                })
            if cur.rowcount == 0:
                return jsonify({"error": "A data e hora têm que ser futuras num incremento de 30 minutos no horário 8-13h ou 14-19h."}), 400
            cur.fetchall()
            try:
                cur.execute(regista_query, (paciente, nif, clinica, data, hora))
            except psycopg.errors.RaiseException as e:
                conn.rollback()
                return jsonify({"error": f"{e.diag.message_primary}"}), 400
            except psycopg.errors.UniqueViolation as e:
                if "consulta_nif_data_hora_key" in str(e):
                    conn.rollback()
                    return jsonify({"error": "O médico já tem uma consulta nesta data e hora."}), 400
                if "consulta_ssn_data_hora_key" in str(e):
                    conn.rollback()
                    return jsonify({"error": "O paciente já tem uma consulta nesta data e hora."}), 400
                else:
                    conn.rollback()
                    return jsonify({"error": f"Erro ao registar consulta: {e.diag.message_primary}"}), 400
            except psycopg.Error as e:
                conn.rollback()
                return jsonify({"error": f"Erro ao registar consulta: {e.diag.primary_message}"}), 500
            except:
                conn.rollback()
                return jsonify({"error": f"Erro interno."}), 500
            finally:
                conn.commit()
            log.debug(f"Marcação registada: paciente {paciente}, medico {medico}, clinica {clinica}, data {data}, hora {hora}")
    
    return jsonify({"success": "Marcação registada com sucesso"}), 200


@app.route("/a/<clinica>/cancelar/", methods=("DELETE",))
def consulta_delete(clinica):
    """Cancela uma marcação de consulta que ainda não se realizou na clínica."""
    
    # Receber os dados da requisição
    paciente = request.json.get('paciente')
    medico = request.json.get('medico')
    data = request.json.get('data')  
    hora = request.json.get('hora')  

    if not paciente:
        return jsonify({"error": "Parâmetro paciente em falta."}), 400
    if not medico:
        return jsonify({"error": "Parâmetro medico em falta."}), 400
    if not data:
        return jsonify({"error": "Parâmetro data em falta."}), 400
    if data and not re.match(r"\d{4}-\d{2}-\d{2}", data):
        return jsonify({"error": "Formato de data inválido."}), 400
    if not hora:
        return jsonify({"error": "Parâmetro hora em falta."}), 400
    if hora and not re.match(r"\d{2}:\d{2}:\d{2}", hora):
        return jsonify({"error": "Formato de hora inválido."}), 400
    
    verifica_data_query = """SELECT 1 
    FROM distinct_horas 
    WHERE (
    (hora > CURRENT_TIMESTAMP::time AND %(data)s=CURRENT_DATE) 
    OR %(data)s>CURRENT_DATE
    ) AND (hora = %(hora)s);
    """

    receita_query = """
    SELECT codigo_sns, id FROM consulta 
    WHERE ssn = %s AND nif = %s AND nome = %s AND data = %s AND hora = %s;
    """

    delete_receita_query = """
    DELETE FROM receita
    WHERE codigo_sns = %s;
    """
    delete_observacao_query= """
    DELETE FROM observacao
    WHERE id = %s"""

    delete_consulta_query = """
    DELETE FROM consulta
    WHERE id = %s;
    """
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(receita_query, (paciente, medico, clinica, data, hora))
            if cur.rowcount == 0:
                return jsonify({"error": "Marcação não encontrada."}), 404
            receita = cur.fetchone()
            cur.execute(verifica_data_query, {
                    "data": data, "hora": hora,
                })
            if cur.rowcount == 0:
                return jsonify({"error": "Não é possível cancelar uma consulta que já ocorreu."}), 400
            try:
                cur.execute(delete_receita_query, (receita.codigo_sns,))
                cur.execute(delete_observacao_query, (receita.id,))
                cur.execute(delete_consulta_query, (receita.id,))
            except psycopg.Error as e:
                conn.rollback()
                return jsonify({"error": f"Erro ao cancelar consulta: {e.diag.primary_message}"}), 500
            except:
                conn.rollback()
                return jsonify({"error": f"Erro interno."}), 500
            conn.commit()
            log.debug(f"Marcação cancelada: paciente {paciente}, medico {medico}, clinica {clinica}, data {data}, hora {hora}")
    
    return jsonify({"success": "Marcação cancelada com sucesso"}), 200


if __name__ == "__main__":
    app.run()
