from psycopg.rows import namedtuple_row
import os
from logging.config import dictConfig
import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row


# DATABASE_URL environment variable if it exists, otherwise use this.
# Format postgres://username:password@hostname/database_name.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://bank: bank@postgres/bank")

@app.route("/", methods=("GET",))
def clinic_index(): 

    query = """
    SELECT nome, morada FROM clinica;
    """   
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            clinics = cur.execute(query, ()).fetchall() 
            log.debug(f"Found {cur.rowcount} rows.")
    
    return jsonify(clinics)


@app.route("/c/<clinica>/ ", methods=("GET",))
def especialidade_index(clinica):
    """Lista todas as especialidades oferecidas na clínica especificada."""
    
    query = """
    SELECT DISTINCT especialidade 
    FROM trabalha t 
    JOIN medico m USING(nif) 
    WHERE t.nome = %s;
    """
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(query, (clinica,))
            especialidades = cur.fetchall()
            log.debug(f"Found {cur.rowcount} rows for clinic {clinica}.")
    
    return jsonify([especialidade.especialidade for especialidade in especialidades])


@app.route("/c/<clinica>/<especialidade>/ ", methods=("GET",))
def medic_index(clinica, especialidade):
   
    query_medicos = """
    SELECT DISTINCT nome 
    FROM trabalha t 
    JOIN medico m USING(nif) 
    WHERE t.nome = %s AND m.especialidade = %s;
    """
    #data e hora ASC ou DESC?
    query_horarios = """
    SELECT data, hora
    FROM consulta
    WHERE nif = %s AND clinica = %s
    ORDER BY data ASC, hora ASC
    LIMIT 3
    """
    
    result = []
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            # Buscar médicos
            cur.execute(query_medicos, (clinica, especialidade))
            medicos = cur.fetchall()
            log.debug(f"Found {cur.rowcount} medicos for clinic {clinica} and specialty {especialidade}.")
            
            for medico in medicos:
                # Buscar horários para cada médico
                cur.execute(query_horarios, (medico.nif, clinica))
                horarios = cur.fetchall()
                result.append({
                    'nome': medico.nome,
                    'horarios': [(horario.data, horario.hora) for horario in horarios]
                })
    
    return jsonify(result)


@app.route("/a/<clinica>/cancelar/", methods=("POST",))
def consulta_delete(clinica):
    """Cancela uma marcação de consulta que ainda não se realizou na clínica."""
    
    # Receber os dados da requisição
    paciente = request.json.get('paciente')
    medico = request.json.get('medico')
    data = request.json.get('data')  
    hora = request.json.get('hora')  
    
    if not paciente or not medico or not data or not hora:
        return jsonify({"error": "Parâmetros em falta"}), 400
    
    delete_query = """
    DELETE FROM consulta
    WHERE ssn = %s AND nif = %s AND nome = %s AND data = %s AND hora = %s;
    """
    
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(delete_query, (paciente, medico, clinica, data, hora))
            if cur.rowcount == 0:
                return jsonify({"error": "Marcação não encontrada"}), 404
            conn.commit()
            log.debug(f"Marcação cancelada: paciente {paciente}, medico {medico}, clinica {clinica}, data {data}, hora {hora}")
    
    return jsonify({"success": "Marcação cancelada com sucesso"}), 200