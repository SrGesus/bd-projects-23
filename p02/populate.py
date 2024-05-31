import random
import datetime
import sys

primeiros_nomes = [ "Afonso", "Beatriz", "Carlos", "Diana", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana", "Joaquim", "Larissa", "Marcos", "Natália", "Otávio", "Paula",  "Quintino", "Raquel", "Sandro", "Tatiana", "Ubirajara", "Valéria", "Washington",  "Xavier", "Iara", "Zeca", "Adriana", "Breno", "Camila", "Daniel", "Elisa", "Fabio",  "Gustavo", "Heloísa", "Isabela", "João", "Cátia", "Leonardo", "Mariana", "Nicolas",  "Olivia", "Pedro", "Margarida", "Renato", "Sofia", "Tiago", "Ursula", "Vitor", "Guilherme",  "Ximena", "Yuri", "Zilda", "Andre", "Bruna", "Claudia", "Diego", "Erica", "Filipe",  "Giovanna", "Humberto", "Ingrid", "José", "Karla", "Luan", "Marta", "Nuno", "Osvaldo",  "Priscila", "Quitéria", "Rafael", "Silvia", "Tadeu", "Ulisses", "Vanessa", "Wagner",  "Xuxa", "Francisca", "Zoraide", "Ana", "Bernardo", "Catarina", "Diogo", "Emanuel",  "Francisco", "Gabriela", "Henrique", "Ivone", "Joana", "Kevin", "Lúcia", "Matheus",  "Neusa", "Oscar", "Patrícia", "Querubina", "Rodrigo", "Simone", "Telma", "Ubiraci",  "Viviane", "Wellington", "Yasmin", "Zé"]
ultimos_nomes = [ "Almeida", "Barbosa", "Cardoso", "Dias", "Evangelista", "Ferreira", "Gomes", "Henrique", "Ibarra", "Jardim", "Klein", "Lima", "Macedo", "Nascimento", "Oliveira", "Pereira",  "Quintana", "Rodrigues", "Santos", "Teixeira", "Uchoa", "Vieira", "Xavier", "Yamamoto",  "Zanetti", "Araújo", "Barros", "Cunha", "Duarte", "Esteves", "Faria", "Gonçalves",  "Hernandez", "Igrejas", "Junqueira", "Kawasaki", "Lopes", "Martins", "Neves",  "Ortega", "Pires", "Queiroz", "Ribeiro", "Silva", "Tavares", "Ulhoa", "Valente",  "Werneck", "Ximenes", "Yanez", "Zara", "Antunes", "Bastos", "Castro", "Diniz",  "Espírito Santo", "Furtado", "Guimarães", "Hidalgo", "Ivo", "Kuhn",  "Lacerda", "Monteiro", "Noronha", "Ornelas", "Pimenta", "Queiroga", "Ramos",  "Souza", "Torres", "Urbano", "Vasconcelos", "Witt", "Yamada", "Zanin",  "Azevedo", "Botelho", "Correia", "Domingues", "Franco", "Gouveia",  "Horta", "Bananeira", "Koch", "Leite", "Marques", "Nogueira", "Pimentel",  "Quirino", "Reis", "Siqueira", "Ulian", "Vidal", "Weber",  "Zanini", "Bittencourt", "Cabral", "Damasceno", "Evaristo", "Freitas",  "Garcia", "Homem", "Inácio", "Carvalho"]
nomes = [f"{primeiro} {ultimo}" for primeiro in primeiros_nomes for ultimo in ultimos_nomes]
nif = 200000000
telefone = 910000000
moradas = [ ["Rua %, 1150-015 Lisboa", 1], ["Rua %, 1100-202 Lisboa", 1], ["Rua %, 2580-649 Carregado", 1], ["Rua %, 2635-018 Rio de Mouro", 1], ["Rua %, 2775-615 Carcavelos", 1]]
especialidades = [
  {"nome": "clínica geral", "num_medicos": 20},
  {"nome": "ortopedia", "num_medicos": 5},
  {"nome": "cardiologia", "num_medicos": 25},
  {"nome": "oncologia", "num_medicos": 5},
  {"nome": "dermatologia", "num_medicos": 3},
  {"nome": "neurologia", "num_medicos": 2},
]

def dict_to_sql(table_name, data):
  """Converts a list of dictionaries of the same type 
  to a list of SQL INSERT statements."""
  statement = [
    f"-- {len(data)} rows for table {table_name}",
    f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES"
  ]
  for row in data:
    values = ', '.join([f"'{value}'" if value != 'NULL' else 'NULL' for value in row.values()])
    statement.append(f"({values}),")
  statement[-1] = statement[-1][:-1] + ';'
  return '\n' + '\n'.join(statement)

def write_to_file(filename, sql_statements):
  with open(filename, 'w') as f:
    for line in sql_statements:
      f.write(line + '\n')
      # print(line)

def generate_clinicas():
  return [
    {"nome": "Centro Clinico dos Anjos", "telefone": "213561336", "morada": "Avenida Almirante Reis 1, 1150-015 Lisboa"},
    {"nome": "Clinica Sorriso Famoso", "telefone": "213472156", "morada": "Rua Augusta 1, 1100-202 Lisboa"},
    {"nome": "Clinica Dentejo", "telefone": "263853342", "morada": "Rua Poço Pedreiro 1, 2580-649 Carregado"},
    {"nome": "Clinica Joaquim Chaves Sintra", "telefone": "214124300", "morada": "Rua Alto do Forte 1, 2635-018 Rio de Mouro"},
    {"nome": "Clinica Sabeanas", "telefone": "218025501", "morada": "Praça Do Junqueiro 1, 2775-615 Carcavelos"}
  ]


def generate_enfermeiros(clinicas):
  enfermeiros = []
  global nif
  global telefone
  for clinica in clinicas:
    for i in range(random.randint(5, 6)):
      morada = moradas[clinicas.index(clinica)][0].replace('%', str(moradas[clinicas.index(clinica)][1]))
      moradas[clinicas.index(clinica)][1] += 1
      enfermeiros.append({
        'nif': str(nif),
        'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
        'telefone': str(telefone),
        'morada': morada,
        'nome_clinica': clinica['nome']
      })
      nif += random.randint(1, 35000)
      telefone += random.randint(1, 20000)
  return enfermeiros

def generate_medicos(especialidades):
  medicos = []
  global nif
  global telefone
  for esp in especialidades:
    for _ in range(esp['num_medicos']):
      i = random.randint(0, len(moradas) - 1)
      morada = moradas[i][0].replace('%', str(moradas[i][1]))
      moradas[i][1] += 1
      medicos.append({
        'nif': str(nif),
        'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
        'telefone': str(telefone),
        'morada': morada,
        'especialidade': esp['nome']
      })
      nif += random.randint(1, 35000)
      telefone += random.randint(1, 20000)
  return medicos

def generate_trabalha(medicos, clinicas):
  while True:
    valid = True
    trabalha = []
    for medico in medicos:
      clinicas_medico_sample = random.sample(clinicas, random.randint(2,4))
      clinicas_medico = [random.choice(clinicas_medico_sample)['nome'] for _ in range(7)]
      while len(set(clinicas_medico)) < 2:
        clinicas_medico = [random.choice(clinicas_medico_sample)['nome'] for _ in range(7)]
      for i in range(7):
        trabalha.append({
          'nif': medico['nif'],
          'nome': clinicas_medico[i],
          'dia_da_semana': i+1
        })
    # Verificar que todas as clinicas têm pelo menos 8 médicos a trabalhar nesse dia da semana
    for clinica in clinicas:
      for dia in range(1, 8):
        if len([t for t in trabalha if t['nome'] == clinica['nome'] and t['dia_da_semana'] == dia]) < 8:
          print("Bruh")
          valid = False
          break
        if not valid: 
          break
    if valid:
      break
  return trabalha

ssn = 10000000000
def generate_pacientes(num_pacientes):
  pacientes = []
  global nif
  global telefone
  global ssn
  for paciente_id in range(1, num_pacientes + 1):
    i = random.randint(0, len(moradas) - 1)
    morada = moradas[i][0].replace('%', str(moradas[i][1]))
    moradas[i][1] += 1
    data_nasc = datetime.date(random.randint(1950, 2006), random.randint(1, 12), random.randint(1, 28)).isoformat()
    pacientes.append({
      'ssn': str(ssn),
      'nif': str(nif),
      'nome': nomes.pop(random.randint(0, len(nomes) - 1)),
      'telefone': str(telefone),
      'morada': morada,
      'data_nasc': data_nasc,
    })
    nif += random.randint(1, 35000)
    telefone += random.randint(1, 20000)
    ssn += random.randint(1, 1000000)
  return pacientes

def generate_consultas(pacientes, trabalha, clinicas, pacientes_cronicos):
  consultas = []
  global nif
  global telefone
  consulta_id = 1
  codigo_sns = 100000000000
  start_date = datetime.date(2023, 1, 1)
  end_date = datetime.date(2024, 12, 31)
  current_date = start_date
  counter = 0
  pacientes_hoje = pacientes.copy()
  pacientes_cronicos_hoje = pacientes_cronicos.copy()
  while current_date <= end_date:
    if counter % 6 == 0:
      pacientes_hoje = pacientes.copy()
      pacientes_cronicos_hoje = pacientes_cronicos.copy()
    for clinica in clinicas:
      dia_da_semana = current_date.weekday() + 1
      medicos_clinica = [t['nif'] for t in trabalha if t['nome'] == clinica['nome'] and t['dia_da_semana'] == dia_da_semana]
      horas = [f'{str(i).zfill(2)}:{j}:00' for i in range(8, 13) for j in ("00", "30")]
      horas += [f'{str(i).zfill(2)}:{j}:00' for i in range(14, 19) for j in ("00", "30")]
      for medico_nif in medicos_clinica:
        # 3 consultas por médico garante que há pelo menos 
        # 21 consultas por dia nesta clínica
        horas_medico = horas.copy()
        for hora in random.sample(horas_medico, random.randint(2, 3)):
          horas_medico.remove(hora)
          consultas.append({
            'id': consulta_id,
            'ssn': pacientes_hoje.pop(random.randint(0, len(pacientes_hoje) - 1))['ssn'],
            'nif': medico_nif,
            'nome': clinica['nome'],
            'data': current_date.isoformat(),
            'hora': hora,
            'codigo_sns': str(codigo_sns).zfill(12)
          })
          consulta_id += 1
          codigo_sns += random.randint(1, 8000)
        for hora in random.sample(horas_medico, 1):
          consultas.append({
            'id': consulta_id,
            'ssn': pacientes_cronicos_hoje.pop(random.randint(0, len(pacientes_cronicos_hoje) - 1))['ssn'],
            'nif': medico_nif,
            'nome': clinica['nome'],
            'data': current_date.isoformat(),
            'hora': hora,
            'codigo_sns': str(codigo_sns).zfill(12)
          })
          consulta_id += 1
          codigo_sns += random.randint(1, 8000)
    current_date += datetime.timedelta(days=1)
    counter += 1
  return consultas

medicamentos = ['Adinazolam', 'Alfentanil', 'Alphenal ', 'Alprazolam', 'Amineptine', 'Aminorex', 'Atamestane', 'Barbital ', 'Bolandiol', 'Bolazine', 'Boldenone', 'Boldione', 'Bolenol', 'Bromazepam', 'Bromazolam', 'Brotizolam', 'Butalbital', 'Butethal ', 'Camazepam', 'Cannabinol', 'Cannabis', 'Sativex', 'Cathinone', 'CBPMs', 'Clobazam', 'Clonazepam', 'Clonazolam', 'Clostebol', 'Cloxazolam', 'Coca leaf', 'Cocaine', 'Codeine', 'Danazol', 'Diazepam', 'Diclazepam', 'Difenoxin', 'Dipipanone', 'Dronabinol', 'Ecgonine', 'Enestebol', 'Epidyolex', 'Estazolam', 'Ethinamate', 'Etizolam', 'Etorphine', 'Fentanyl', 'Flurazepam', 'Fonazepam', 'Furazabol', 'Gestrinone', 'Halazepam', 'Hexethal', 'Ketamine', 'Ketazolam', 'Khat', 'Lefetamine', 'Lofentanil', 'Loprazolam', 'Lorazepam', 'Lysergide ', 'Mazindol', 'Mebolazine', 'Medazepam', 'Mefenorex', 'Mesabolone', 'Mescaline', 'Mesocarb', 'Metazocine', 'Methadone', 'Metizolam', 'Metopon', 'Mibolerone', 'Midazolam', 'Morphine', 'Myrophine', 'Nabilone', 'Nandrolone', 'Nicocodine', 'Nifoxipam', 'Nitrazepam', 'Nitrazolam', 'Norcocaine', 'Norcodeine', 'Nordazepam', 'Opium', 'Oripavine', 'Oxabolone', 'Oxazepam', 'Oxazolam', 'Oxycodone', 'Pemoline', 'Pethidine ', 'Piminodine', 'Pinazepam', 'Pipradrol', 'Prazepam', 'Propiram', 'Psilocin', 'Pyrazolam', 'Quinbolone', 'Roxibolone', 'Silandrone', 'Somatrem', 'Somatropin', 'Stanolone', 'Stanozolol', 'Stenbolone', 'Sufentanil', 'Talbutal', 'Tapentadol', 'Temazepam', 'Tetrazepam', 'Thebacon ', 'Thebaine', 'Tilidine', 'Tramadol', 'Trenbolone', 'Triazolam', 'Zaleplon', 'Zeranol', 'Zilpaterol', 'Zipeprol', 'Zolpidem', 'Zopiclone']



medicamentos_especialidade = {
  esp: random.sample(medicamentos, random.randint(6, 10)) for esp in [e['nome'] for e in especialidades]
}

def generate_receitas(consultas, medicos):
  receitas = []
  for consulta in consultas:
    esp = [m['especialidade'] for m in medicos if m['nif'] == consulta['nif']][0]
    if random.random() < 0.8:
      for medicamento in random.sample(medicamentos_especialidade[esp], random.randint(1, 6)):
        receitas.append({
          'codigo_sns': consulta['codigo_sns'],
          'medicamento': medicamento,
          'quantidade': random.randint(1, 3)
        })
    else: 
      consulta['codigo_sns'] = 'NULL'
  return receitas

sintomas_qualitativos = [
  "Dor de cabeça", "Náusea", "Tontura", "Fadiga", "Febre", "Calafrios", "Sudorese", 
  "Tosse", "Dor no peito", "Falta de ar", "Dor abdominal", "Diarreia", "Constipação", 
  "Vômito", "Arrepios", "Perda de apetite", "Perda de peso", "Ganho de peso", 
  "Erupção cutânea", "Coceira", "Inchaço", "Dores musculares", "Dores articulares", 
  "Palpitações", "Ansiedade", "Depressão", "Confusão", "Insônia", "Sonolência", 
  "Fraqueza", "Amarelamento da pele", "Olhos vermelhos", "Dor de garganta", 
  "Rouquidão", "Congestão nasal", "Nariz escorrendo", "Dificuldade para engolir", 
  "Perda de olfato", "Perda de paladar", "Zumbido nos ouvidos", "Visão turva", 
  "Olhos secos", "Lacrimejamento", "Dor de dente", "Sangramento nas gengivas", 
  "Cãibras", "Dor nas costas", "Dor pélvica", "Dor nas pernas", "Falta de coordenação"
]

sintomas_quantitativos = [
  {"sintoma": "Batimentos cardíacos por minuto", "min": 60, "max": 100},
  {"sintoma": "Pressão arterial sistólica", "min": 90, "max": 160},
  {"sintoma": "Pressão arterial diastólica", "min": 55, "max": 120},
  {"sintoma": "Nível de glicose no sangue (mg/dL)", "min": 70, "max": 140},
  {"sintoma": "Temperatura corporal (°C)", "min": 36.1, "max": 37.2},
  {"sintoma": "Saturação de oxigênio (%)", "min": 95, "max": 100},
  {"sintoma": "Frequência respiratória (respirações por minuto)", "min": 12, "max": 20},
  {"sintoma": "Índice de massa corporal (IMC)", "min": 18.5, "max": 24.9},
  {"sintoma": "Colesterol total (mg/dL)", "min": 125, "max": 200},
  {"sintoma": "Triglicerídeos (mg/dL)", "min": 50, "max": 150},
  {"sintoma": "Nível de creatinina no sangue (mg/dL)", "min": 0.6, "max": 1.3},
  {"sintoma": "Volume urinário (mL por dia)", "min": 800, "max": 2000},
  {"sintoma": "Hemoglobina (g/dL)", "min": 13.8, "max": 17.2},
  {"sintoma": "Hematócrito (%)", "min": 40.7, "max": 50.3},
  {"sintoma": "Número de leucócitos (milhões por mL)", "min": 4, "max": 11},
  {"sintoma": "Número de plaquetas (milhões por mL)", "min": 150, "max": 450},
  {"sintoma": "pH sanguíneo", "min": 7.35, "max": 7.45},
  {"sintoma": "Nível de cálcio no sangue (mg/dL)", "min": 8.5, "max": 10.5},
  {"sintoma": "Nível de sódio no sangue (mEq/L)", "min": 135, "max": 145},
  {"sintoma": "Nível de potássio no sangue (mEq/L)", "min": 3.5, "max": 5.0}
]

def generate_observacoes(consultas):
  observacoes = []
  for consulta in consultas:
    # 1 a 5 sintomas qualitativos
    for sintoma in random.sample(sintomas_qualitativos, random.randint(1, 5)):
      observacoes.append({
        'id': consulta['id'],
        'parametro': sintoma,
        'valor': 'NULL'
      })
    # 0 a 3 sintomas quantitativos
    for sintoma in random.sample(sintomas_quantitativos, random.randint(0, 3)):
      valor = random.normalvariate((sintoma['min'] + sintoma['max']) / 2, (sintoma['max'] - sintoma['min']) / 6)
      observacoes.append({
        'id': consulta['id'],
        'parametro': sintoma['sintoma'],
        'valor': f'{valor:.2f}'
      })
  return observacoes

def main():
  sql_statements = [
    "-- Eliminar dados anteriores",
    "TRUNCATE TABLE receita, observacao, consulta, trabalha, paciente, medico, enfermeiro, clinica RESTART IDENTITY;"
  ]
  clinicas = generate_clinicas()
  medicos = generate_medicos(especialidades)
  trabalha = generate_trabalha(medicos, clinicas)
  pacientes = generate_pacientes(4640)
  pacientes_cronicos = generate_pacientes(360)
  consultas = generate_consultas(pacientes, trabalha, clinicas, pacientes_cronicos)
  receitas = generate_receitas(consultas, medicos)
  observacoes = generate_observacoes(consultas)
  sql_statements.append(dict_to_sql('clinica', clinicas))
  sql_statements.append(dict_to_sql('enfermeiro', generate_enfermeiros(clinicas)))
  sql_statements.append(dict_to_sql('medico', medicos))
  sql_statements.append(dict_to_sql('trabalha', trabalha))
  sql_statements.append(dict_to_sql('paciente', pacientes+pacientes_cronicos))
  [c.pop('id') for c in consultas]
  sql_statements.append(dict_to_sql('consulta', consultas))
  sql_statements.append(dict_to_sql('receita', receitas))
  sql_statements.append(dict_to_sql('observacao', observacoes))
  sql_statements.append("""
    DROP TABLE distinct_horas;
    CREATE TABLE distinct_horas AS
    SELECT DISTINCT hora
    FROM consulta ORDER BY hora;
  """)
  write_to_file('./data/populate.sql', sql_statements)

if __name__ == '__main__':
  main()
