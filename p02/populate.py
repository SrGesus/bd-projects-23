import random
import datetime

def generate_clinicas():
  nomes = [ 'Centro Clinico dos Anjos', 'Clinica Sorriso Famoso', 
    'Clinica Dentejo', 'Clinica Joaquim Chaves Sintra', 'Clinica Sabeanas']
  telefones = [ '213561336', '213472156', '263853342', '214124300', '218025501']
  moradas = [
    'Avenida Almirante Reis 133, 1150-015 Lisboa', 
    'Rua Augusta 280, 1100-202 Lisboa', 
    'Rua Poço Pedreiro, 2580-649 Carregado', 
    'Rua Alto do Forte IC 19, 2635-018 Rio de Mouro', 
    'Praça Do Junqueiro 4, 2775-615 Carcavelos'
  ]
  sql_statements = []
  for i in range(5):
    sql_statements.append(f"INSERT INTO clinica (nome, telefone, morada) VALUES ('{nomes[i]}', '{telefones[i]}', '{moradas[i]}');")
  return sql_statements

def generate_enfermeiros(clinicas):
  sql_statements = []
  enfermeiro_id = 1
  for clinica in clinicas:
    for i in range(random.randint(5, 6)):
      nif = str(enfermeiro_id).zfill(9)
      nome = f'Enfermeiro {enfermeiro_id}'
      telefone = f'91000000{i}'
      morada = f'Rua F, 1000-00{i} Lisboa'
      sql_statements.append(f"INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES ('{nif}', '{nome}', '{telefone}', '{morada}', '{clinica}');")
      enfermeiro_id += 1
  return sql_statements

def generate_medicos(especialidades):
  sql_statements = []
  medico_id = 1
  for especialidade in especialidades:
    for i in range(20 if especialidade == 'clínica geral' else 8):
      nif = str(medico_id).zfill(9)
      nome = f'Medico {medico_id}'
      telefone = f'92000000{i}'
      morada = f'Rua G, 1000-00{i} Lisboa'
      sql_statements.append(f"INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES ('{nif}', '{nome}', '{telefone}', '{morada}', '{especialidade}');")
      medico_id += 1
  return sql_statements

def generate_trabalha(medicos, clinicas):
  sql_statements = []
  dias_semana = [0, 1, 2, 3, 4, 5, 6]  # 0 = domingo, 6 = sábado
  for clinica in clinicas:
    for medico in medicos:
      dias_trabalho = random.sample(dias_semana, 2)
      for dia in dias_trabalho:
        sql_statements.append(f"INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES ('{medico}', '{clinica}', {dia});")
  return sql_statements

def generate_pacientes(num_pacientes):
  sql_statements = []
  for paciente_id in range(1, num_pacientes + 1):
    ssn = str(paciente_id).zfill(11)
    nif = str(paciente_id).zfill(9)
    nome = f'Paciente {paciente_id}'
    telefone = f'93000000{paciente_id % 10}'
    morada = f'Rua H, 1000-00{paciente_id % 10} Lisboa'
    data_nasc = (datetime.date(1980, 1, 1) + datetime.timedelta(days=paciente_id % 365)).isoformat()
    sql_statements.append(f"INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES ('{ssn}', '{nif}', '{nome}', '{telefone}', '{morada}', '{data_nasc}');")
  return sql_statements

def generate_consultas(num_consultas, pacientes, medicos, clinicas):
  sql_statements = []
  consulta_id = 1
  start_date = datetime.date(2023, 1, 1)
  end_date = datetime.date(2024, 12, 31)
  date_range = (end_date - start_date).days

  for clinica in clinicas:
    for day in range(date_range):
      data_consulta = (start_date + datetime.timedelta(days=day)).isoformat()
      for hour in range(8, 18):
        for half_hour in [0, 30]:
          hora_consulta = f'{hour:02d}:{half_hour:02d}:00'
          for i in range(20):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            codigo_sns = str(consulta_id).zfill(12)
            sql_statements.append(f"INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES ('{paciente}', '{medico}', '{clinica}', '{data_consulta}', '{hora_consulta}', '{codigo_sns}');")
            consulta_id += 1
  return sql_statements

def generate_receitas(consultas):
  receitas = []
  for consulta in consultas:
    if random.random() < 0.8:
      for j in range(random.randint(1, 6)):
        quantidade = random.randint(1, 3)
        medicamento = random.choice(medicamentos)
        receitas.append(f"INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES ('{consulta}', '{medicamento}', {quantidade});")
  return receitas

def generate_observacoes(consultas):
  sql_statements = []
  sintomas = ['Febre', 'Tosse', 'Dor de cabeça', 'Cansaço', 'Dificuldade em respirar']
  metricas = ['Pressão arterial', 'Temperatura corporal', 'Frequência cardíaca']
  
  for consulta in consultas:
    for k in range(random.randint(1, 5)):
      parametro = random.choice(sintomas)
      sql_statements.append(f"INSERT INTO observacao (id, parametro) VALUES ('{consulta}', '{parametro}');")
    for l in range(random.randint(0, 3)):
      parametro = random.choice(metricas)
      valor = random.uniform(50, 150)
      sql_statements.append(f"INSERT INTO observacao (id, parametro, valor) VALUES ('{consulta}', '{parametro}', {valor});")
  return sql_statements

def main():
  clinicas = [
    'Centro Clinico dos Anjos', 
    'Clinica Sorriso Famoso', 
    'Clinica Dentejo', 
    'Clinica Joaquim Chaves Sintra', 
    'Clinica Sabeanas'
  ]
  especialidades = ['clínica geral', 'ortopedia', 'cardiologia', 'dermatologia', 'neurologia', 'pediatria']

  sql_statements = []
  sql_statements += generate_clinicas()
  sql_statements += generate_enfermeiros(clinicas)
  sql_statements += generate_medicos(especialidades)
  medicos = [str(i).zfill(9) for i in range(1, 61)]
  sql_statements += generate_trabalha(medicos, clinicas)
  pacientes = [str(i).zfill(11) for i in range(1, 5001)]
  sql_statements += generate_pacientes(5000)
  consultas = [str(i).zfill(12) for i in range(1, 100001)]  # Número de consultas ajustado para ser realista
  sql_statements += generate_consultas(100000, pacientes, medicos, clinicas)
  sql_statements += generate_receitas(consultas)
  sql_statements += generate_observacoes(consultas)

  with open('populate_db.sql', 'w') as f:
    for statement in sql_statements:
      f.write(statement + '\n')

if __name__ == "__main__":
  main()
