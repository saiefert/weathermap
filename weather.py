from flask import Flask, request
import pandas as pd
import numpy as np
import requests
import random
import json

app = Flask(__name__)


@app.route('/city')
def search_city():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'
    city = request.args.get('q')  # city name passed as argument

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=pt_br&APPID={API_KEY}'
    response = requests.get(url).json()

    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat=-20.44&lon=-54.65&units=metric&' \
           f'lang=pt_br&exclude=minutely,hourly&appid={API_KEY}'
    response2 = requests.get(url2).json()

    current_temperature = response.get('main', {}).get('temp')
    current_temperature_celsius = round(current_temperature - 273.15, 2)

    min_temperature = response.get('main', {}).get('temp_min')
    min_temperature_celsius = round(min_temperature - 273.15, 2)

    max_temperature = response.get('main', {}).get('temp_max')
    max_temperature_celsius = round(max_temperature - 273.15, 2)

    feels_temp = response.get('main', {}).get('feels_like')
    feels_temp_celsius = round(feels_temp - 273.15, 2)

    humidity = response.get('main', {}).get('humidity')

    weather = response.get('weather', {})

    df = pd.DataFrame(weather)
    new_dict = pd.DataFrame.to_dict(df)

    clima = json.dumps(new_dict['main'])
    clima = clima[6:len(clima) - 1]

    descricao = json.dumps(new_dict['description'])
    descricao = descricao[6:len(descricao) - 1]

    if response2.get('cod') == 200:
        alerts = response2.get('alerts', {})

        df_2 = pd.DataFrame(alerts)
        new_dict2 = pd.DataFrame.to_dict(df_2)

        alerta = json.dumps(new_dict2['event'])
        alerta = alerta[6:len(alerta) - 1]

        description = json.dumps(new_dict2['description'])
        description = description[6:len(description) - 1]

        dados = {
            'cidade': city.title(),
            'temperatura': current_temperature_celsius,
            'minima': min_temperature_celsius,
            'maxima': max_temperature_celsius,
            'sensacao termica': feels_temp_celsius,
            'umidade do ar': humidity,
            'clima': clima,
            'descricao': descricao,
            'alerta': alerta,
            'alerta_description': description
        }
    else:
        dados = {
            'cidade': city.title(),
            'temperatura': current_temperature_celsius,
            'minima': min_temperature_celsius,
            'maxima': max_temperature_celsius,
            'sensacao termica': feels_temp_celsius,
            'umidade do ar': humidity,
            'clima': clima,
            'descricao': descricao,
            'alerta': 'Sem alertas na região'
        }

    dados_json = json.dumps(dados)

    return dados_json


@app.route('/leste_ms')
def random_leste():
    API_KEY = 'b38e5304dac486c2728762b73c8ccf21'

    leste = ['bataguassu', 'Angelica', 'ivinhema', 'novo horizonte do sul',
             'anaurilandia', 'Bataypora', 'Taquarussu','Cassilandia', 'inocencia', 'Paranaiba',
             'Aparecida do Taboado', 'Agua Clara', 'Santa Rita do Pardo', 'Ribas do Rio Pardo',
             'Brasilandia']

    cidades = random.sample(leste, 5)

    x = 0
    output_list = []

    while x < 5:
        city = cidades[x]
        municipio = [city.title()]
        municipios = pd.read_csv('municipios_ms.csv')

        lat = municipios['latitude'].loc[municipios['cidade'].isin(municipio)]
        lat = lat.values
        lat = lat[0]
        lon = municipios['longitude'].loc[municipios['cidade'].isin(municipio)]
        lon = lon.values
        lon = lon[0]

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
              f'&exclude=minutely,hourly&appid={API_KEY}'

        response = requests.get(url).json()

        temp = response.get('daily', {})

        temperatura = pd.DataFrame(temp)

        # inicio dos dados do clima hoje
        hoje = temperatura.iloc[0]
        tempo_hoje = hoje.weather[0]
        temp_dia = hoje.temp['day']
        min_hoje = hoje.temp['min']
        max_hoje = hoje.temp['max']
        hum_hoje = hoje.humidity
        clima_hoje = tempo_hoje['main']
        descricao_hoje = tempo_hoje['description']
        pop_hoje = hoje['pop']
        if 'rain' in hoje:
            chuva_hoje = hoje.rain
            chuva_hoje = float(chuva_hoje)
        else:
            chuva_hoje = None
        # fim dos dados do clima hoje

        # inicio dos dados do clima amanha
        amanha = temperatura.iloc[1]
        tempo_amanha = amanha.weather[0]
        temp_amanha = amanha.temp['day']
        min_amanha = amanha.temp['min']
        max_amanha = amanha.temp['max']
        hum_amanha = amanha.humidity
        clima_amanha = tempo_amanha['main']
        descricao_amanha = tempo_amanha['description']
        pop_amanha = amanha['pop']
        if 'rain' in amanha:
            chuva_amanha = amanha.rain
            chuva_amanha = float(chuva_amanha)
        else:
            chuva_amanha = None

        dados = {
            'cidade': city.title(),
            'hoje': 'hoje',
            'temp_dia_hoje': float(temp_dia),
            'minima_hoje': float(min_hoje),
            'maxima_hoje': float(max_hoje),
            'humidade_hoje': float(hum_hoje),
            'clima_hoje': clima_hoje,
            'descricao_clima_hoje': descricao_hoje,
            'possibilidade_de_chuva_hoje': float(pop_hoje),
            'precipitacao_hoje': chuva_hoje,
            'amanha': 'amanha',
            'temp_dia_amanha': float(temp_amanha),
            'minima_amanha': float(min_amanha),
            'maxima_amanha': float(max_amanha),
            'humidade_amanha': float(hum_amanha),
            'clima_amanha': clima_amanha,
            'descricao_clima_amanha': descricao_amanha,
            'possibilidade_de_chuva_amanha': float(pop_amanha),
            'precipitacao_amanha': chuva_amanha
        }

        output_list.append(dados)
        x = x + 1

    dados_json = json.dumps(output_list)
    return dados_json


@app.route('/oeste_ms')
def random_oeste():
    API_KEY = 'b38e5304dac486c2728762b73c8ccf21'

    oeste = ['Ladario', 'Miranda', 'Aquidauana', 'Anastacio',
             'Porto Murtinho', 'Bonito', 'bodoquena', 'Caracol', 'Jardim',
             'Bela Vista', 'Nioaque','Guia Lopes da Laguna']

    cidades = random.sample(oeste, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        municipio = [city.title()]
        municipios = pd.read_csv('municipios_ms.csv')

        lat = municipios['latitude'].loc[municipios['cidade'].isin(municipio)]
        lat = lat.values
        lat = lat[0]
        lon = municipios['longitude'].loc[municipios['cidade'].isin(municipio)]
        lon = lon.values
        lon = lon[0]

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
              f'&exclude=minutely,hourly&appid={API_KEY}'

        response = requests.get(url).json()

        temp = response.get('daily', {})

        temperatura = pd.DataFrame(temp)

        # inicio dos dados do clima hoje
        hoje = temperatura.iloc[0]
        tempo_hoje = hoje.weather[0]
        temp_dia = hoje.temp['day']
        min_hoje = hoje.temp['min']
        max_hoje = hoje.temp['max']
        hum_hoje = hoje.humidity
        clima_hoje = tempo_hoje['main']
        descricao_hoje = tempo_hoje['description']
        pop_hoje = hoje['pop']
        if 'rain' in hoje:
            chuva_hoje = hoje.rain
            chuva_hoje = float(chuva_hoje)
        else:
            chuva_hoje = None
        # fim dos dados do clima hoje

        # inicio dos dados do clima amanha
        amanha = temperatura.iloc[1]
        tempo_amanha = amanha.weather[0]
        temp_amanha = amanha.temp['day']
        min_amanha = amanha.temp['min']
        max_amanha = amanha.temp['max']
        hum_amanha = amanha.humidity
        clima_amanha = tempo_amanha['main']
        descricao_amanha = tempo_amanha['description']
        pop_amanha = amanha['pop']
        if 'rain' in amanha:
            chuva_amanha = amanha.rain
            chuva_amanha = float(chuva_amanha)
        else:
            chuva_amanha = None

        dados = {
            'cidade': city.title(),
            'hoje': 'hoje',
            'temp_dia_hoje': float(temp_dia),
            'minima_hoje': float(min_hoje),
            'maxima_hoje': float(max_hoje),
            'humidade_hoje': float(hum_hoje),
            'clima_hoje': clima_hoje,
            'descricao_clima_hoje': descricao_hoje,
            'possibilidade_de_chuva_hoje': float(pop_hoje),
            'precipitacao_hoje': chuva_hoje,
            'amanha': 'amanha',
            'temp_dia_amanha': float(temp_amanha),
            'minima_amanha': float(min_amanha),
            'maxima_amanha': float(max_amanha),
            'humidade_amanha': float(hum_amanha),
            'clima_amanha': clima_amanha,
            'descricao_clima_amanha': descricao_amanha,
            'possibilidade_de_chuva_amanha': float(pop_amanha),
            'precipitacao_amanha': chuva_amanha
        }

        output_list.append(dados)
        x = x + 1

    dados_json = json.dumps(output_list)
    return dados_json


@app.route('/central_ms')
def random_central():
    API_KEY = 'b38e5304dac486c2728762b73c8ccf21'

    central = ['Rio Negro', 'Corguinho', 'Rochedo', 'Terenos',
               'jaraguari', 'dois irmaos do buriti', 'Sidrolandia', 'nova alvorada do sul']

    cidades = random.sample(central, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        municipio = [city.title()]
        municipios = pd.read_csv('municipios_ms.csv')

        lat = municipios['latitude'].loc[municipios['cidade'].isin(municipio)]
        lat = lat.values
        lat = lat[0]
        lon = municipios['longitude'].loc[municipios['cidade'].isin(municipio)]
        lon = lon.values
        lon = lon[0]

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
              f'&exclude=minutely,hourly&appid={API_KEY}'

        response = requests.get(url).json()

        temp = response.get('daily', {})

        temperatura = pd.DataFrame(temp)

        # inicio dos dados do clima hoje
        hoje = temperatura.iloc[0]
        tempo_hoje = hoje.weather[0]
        temp_dia = hoje.temp['day']
        min_hoje = hoje.temp['min']
        max_hoje = hoje.temp['max']
        hum_hoje = hoje.humidity
        clima_hoje = tempo_hoje['main']
        descricao_hoje = tempo_hoje['description']
        pop_hoje = hoje['pop']
        if 'rain' in hoje:
            chuva_hoje = hoje.rain
            chuva_hoje = float(chuva_hoje)
        else:
            chuva_hoje = None
        # fim dos dados do clima hoje

        # inicio dos dados do clima amanha
        amanha = temperatura.iloc[1]
        tempo_amanha = amanha.weather[0]
        temp_amanha = amanha.temp['day']
        min_amanha = amanha.temp['min']
        max_amanha = amanha.temp['max']
        hum_amanha = amanha.humidity
        clima_amanha = tempo_amanha['main']
        descricao_amanha = tempo_amanha['description']
        pop_amanha = amanha['pop']
        if 'rain' in amanha:
            chuva_amanha = amanha.rain
            chuva_amanha = float(chuva_amanha)
        else:
            chuva_amanha = None

        dados = {
            'cidade': city.title(),
            'hoje': 'hoje',
            'temp_dia_hoje': float(temp_dia),
            'minima_hoje': float(min_hoje),
            'maxima_hoje': float(max_hoje),
            'humidade_hoje': float(hum_hoje),
            'clima_hoje': clima_hoje,
            'descricao_clima_hoje': descricao_hoje,
            'possibilidade_de_chuva_hoje': float(pop_hoje),
            'precipitacao_hoje': chuva_hoje,
            'amanha': 'amanha',
            'temp_dia_amanha': float(temp_amanha),
            'minima_amanha': float(min_amanha),
            'maxima_amanha': float(max_amanha),
            'humidade_amanha': float(hum_amanha),
            'clima_amanha': clima_amanha,
            'descricao_clima_amanha': descricao_amanha,
            'possibilidade_de_chuva_amanha': float(pop_amanha),
            'precipitacao_amanha': chuva_amanha
        }

        output_list.append(dados)
        x = x + 1

    dados_json = json.dumps(output_list)
    return dados_json

@app.route('/norte_ms')
def random_norte():
    API_KEY = 'b38e5304dac486c2728762b73c8ccf21'

    norte = ['Paraiso das Aguas', 'chapadao do sul', 'Sonora', 'Pedro Gomes',
             'Coxim', 'Rio Verde de Mato Grosso', 'sao gabriel do oeste',
             'Camapua', 'alcinopolis', 'Costa Rica', 'Figueirao', 'Bandeirantes']

    cidades = random.sample(norte, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        municipio = [city.title()]
        municipios = pd.read_csv('municipios_ms.csv')

        lat = municipios['latitude'].loc[municipios['cidade'].isin(municipio)]
        lat = lat.values
        lat = lat[0]
        lon = municipios['longitude'].loc[municipios['cidade'].isin(municipio)]
        lon = lon.values
        lon = lon[0]

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
              f'&exclude=minutely,hourly&appid={API_KEY}'

        response = requests.get(url).json()

        temp = response.get('daily', {})

        temperatura = pd.DataFrame(temp)

        # inicio dos dados do clima hoje
        hoje = temperatura.iloc[0]
        tempo_hoje = hoje.weather[0]
        temp_dia = hoje.temp['day']
        min_hoje = hoje.temp['min']
        max_hoje = hoje.temp['max']
        hum_hoje = hoje.humidity
        clima_hoje = tempo_hoje['main']
        descricao_hoje = tempo_hoje['description']
        pop_hoje = hoje['pop']
        if 'rain' in hoje:
            chuva_hoje = hoje.rain
            chuva_hoje = float(chuva_hoje)
        else:
            chuva_hoje = None
        # fim dos dados do clima hoje

        # inicio dos dados do clima amanha
        amanha = temperatura.iloc[1]
        tempo_amanha = amanha.weather[0]
        temp_amanha = amanha.temp['day']
        min_amanha = amanha.temp['min']
        max_amanha = amanha.temp['max']
        hum_amanha = amanha.humidity
        clima_amanha = tempo_amanha['main']
        descricao_amanha = tempo_amanha['description']
        pop_amanha = amanha['pop']
        if 'rain' in amanha:
            chuva_amanha = amanha.rain
            chuva_amanha = float(chuva_amanha)
        else:
            chuva_amanha = None

        dados = {
            'cidade': city.title(),
            'hoje': 'hoje',
            'temp_dia_hoje': float(temp_dia),
            'minima_hoje': float(min_hoje),
            'maxima_hoje': float(max_hoje),
            'humidade_hoje': float(hum_hoje),
            'clima_hoje': clima_hoje,
            'descricao_clima_hoje': descricao_hoje,
            'possibilidade_de_chuva_hoje': float(pop_hoje),
            'precipitacao_hoje': chuva_hoje,
            'amanha': 'amanha',
            'temp_dia_amanha': float(temp_amanha),
            'minima_amanha': float(min_amanha),
            'maxima_amanha': float(max_amanha),
            'humidade_amanha': float(hum_amanha),
            'clima_amanha': clima_amanha,
            'descricao_clima_amanha': descricao_amanha,
            'possibilidade_de_chuva_amanha': float(pop_amanha),
            'precipitacao_amanha': chuva_amanha
        }

        output_list.append(dados)
        x = x + 1

    dados_json = json.dumps(output_list)
    return dados_json

@app.route('/sul_ms')
def random_sul():
    API_KEY = 'b38e5304dac486c2728762b73c8ccf21'

    sul = ['Maracaju', 'Rio Brilhante', 'Itapora', 'douradina',  'jatei',
           'fatima do sul', 'deodapolis', 'Caarapo', 'Vicentina', 'gloria de dourados',
           'Juti', 'Navirai', 'itaquirai', 'Iguatemi', 'Japora', 'Eldorado', 'Mundo Novo',
           'Nova Andradina', 'antonio joao', 'Laguna Carapa', 'Aral Moreira', 'Amambai',
           'Coronel Sapucaia', 'Tacuru', 'Paranhos', 'Sete Quedas']

    cidades = random.sample(sul, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        municipio = [city.title()]
        municipios = pd.read_csv('municipios_ms.csv')

        lat = municipios['latitude'].loc[municipios['cidade'].isin(municipio)]
        lat = lat.values
        lat = lat[0]
        lon = municipios['longitude'].loc[municipios['cidade'].isin(municipio)]
        lon = lon.values
        lon = lon[0]

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
              f'&exclude=minutely,hourly&appid={API_KEY}'

        response = requests.get(url).json()

        temp = response.get('daily', {})

        temperatura = pd.DataFrame(temp)

        # inicio dos dados do clima hoje
        hoje = temperatura.iloc[0]
        tempo_hoje = hoje.weather[0]
        temp_dia = hoje.temp['day']
        min_hoje = hoje.temp['min']
        max_hoje = hoje.temp['max']
        hum_hoje = hoje.humidity
        clima_hoje = tempo_hoje['main']
        descricao_hoje = tempo_hoje['description']
        pop_hoje = hoje['pop']
        if 'rain' in hoje:
            chuva_hoje = hoje.rain
            chuva_hoje = float(chuva_hoje)
        else:
            chuva_hoje = None
        # fim dos dados do clima hoje

        # inicio dos dados do clima amanha
        amanha = temperatura.iloc[1]
        tempo_amanha = amanha.weather[0]
        temp_amanha = amanha.temp['day']
        min_amanha = amanha.temp['min']
        max_amanha = amanha.temp['max']
        hum_amanha = amanha.humidity
        clima_amanha = tempo_amanha['main']
        descricao_amanha = tempo_amanha['description']
        pop_amanha = amanha['pop']
        if 'rain' in amanha:
            chuva_amanha = amanha.rain
            chuva_amanha = float(chuva_amanha)
        else:
            chuva_amanha = None

        dados = {
            'cidade': city.title(),
            'hoje': 'hoje',
            'temp_dia_hoje': float(temp_dia),
            'minima_hoje': float(min_hoje),
            'maxima_hoje': float(max_hoje),
            'humidade_hoje': float(hum_hoje),
            'clima_hoje': clima_hoje,
            'descricao_clima_hoje': descricao_hoje,
            'possibilidade_de_chuva_hoje': float(pop_hoje),
            'precipitacao_hoje': chuva_hoje,
            'amanha': 'amanha',
            'temp_dia_amanha': float(temp_amanha),
            'minima_amanha': float(min_amanha),
            'maxima_amanha': float(max_amanha),
            'humidade_amanha': float(hum_amanha),
            'clima_amanha': clima_amanha,
            'descricao_clima_amanha': descricao_amanha,
            'possibilidade_de_chuva_amanha': float(pop_amanha),
            'precipitacao_amanha': chuva_amanha
        }

        output_list.append(dados)
        x = x + 1

    dados_json = json.dumps(output_list)
    return dados_json


@app.route('/')
def index():
    return '<h1>TV Morena</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
