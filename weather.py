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


@app.route('/leste')
def random_leste():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    leste = ['bataguassu', 'Angélica', 'ivinhema', 'novo horizonte do sul',
             'anaurilândia', 'Bataiporã', 'Taquarussu','Cassilândia', 'inocência', 'Paranaíba',
             'Aparecida do Taboado', 'Água Clara', 'Santa Rita do Pardo', 'Ribas do Rio Pardo',
             'Brasilândia']

    cidades = random.sample(leste, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        url2 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url2).json()

        if response.get('cod') != 200:
            municipio = [city.title()]
            municipios = pd.read_csv("municipios_rmc.csv")
            lat = municipios['latitude'].loc[municipios['nome'].isin(municipio)]
            lat = float(lat)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon)
            url3 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_KEY}'
            response_2 = requests.get(url3).json()
            current_temperature = response_2.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response_2.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response_2.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response_2.get('main', {}).get('humidity')

            weather = response_2.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)

        else:
            current_temperature = response.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response.get('main', {}).get('humidity')

            weather = response.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)
        dados_json = json.dumps(output_list)
        x = x + 1

    return dados_json


@app.route('/oeste')
def random_oeste():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    oeste = ['Ladário', 'Miranda', 'Aquidauana', 'Anastácio',
             'Porto Murtinho', 'Bonito', 'bodoquena', 'Caracol', 'Jardim',
             'Bela Vista', 'Nioaque','Guia Lopes da Laguna']

    cidades = random.sample(oeste, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        url2 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url2).json()

        if response.get('cod') != 200:
            municipio = [city.title()]
            municipios = pd.read_csv("municipios_rmc.csv")
            lat = municipios['latitude'].loc[municipios['nome'].isin(municipio)]
            lat = float(lat)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon)
            url3 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_KEY}'
            response_2 = requests.get(url3).json()
            current_temperature = response_2.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response_2.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response_2.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response_2.get('main', {}).get('humidity')

            weather = response_2.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)

        else:
            current_temperature = response.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response.get('main', {}).get('humidity')

            weather = response.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)
        dados_json = json.dumps(output_list)
        x = x + 1

    return dados_json


@app.route('/central')
def random_central():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    central = ['Rio Negro', 'Corguinho', 'Rochedo', 'Terenos',
               'jaraguari', 'dois irmãos do buriti', 'Sidrolândia', 'nova alvorada do sul']

    cidades = random.sample(central, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        url2 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url2).json()

        if response.get('cod') != 200:
            municipio = [city.title()]
            municipios = pd.read_csv("municipios_rmc.csv")
            lat = municipios['latitude'].loc[municipios['nome'].isin(municipio)]
            lat = float(lat)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon)
            url3 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_KEY}'
            response_2 = requests.get(url3).json()
            current_temperature = response_2.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response_2.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response_2.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response_2.get('main', {}).get('humidity')

            weather = response_2.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)

        else:
            current_temperature = response.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response.get('main', {}).get('humidity')

            weather = response.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)
        dados_json = json.dumps(output_list)
        x = x + 1

    return dados_json

@app.route('/norte')
def random_norte():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    norte = ['Paraíso das Águas', 'chapadão do sul', 'Sonora', 'Pedro Gomes',
             'Coxim', 'Rio Verde de Mato Grosso', 'são gabriel do oeste',
             'Camapuã', 'alcinópolis', 'Costa Rica', 'Figueirão', 'Bandeirantes']

    cidades = random.sample(norte, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        url2 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url2).json()

        if response.get('cod') != 200:
            municipio = [city.title()]
            municipios = pd.read_csv("municipios_rmc.csv")
            lat = municipios['latitude'].loc[municipios['nome'].isin(municipio)]
            lat = float(lat)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon)
            url3 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_KEY}'
            response_2 = requests.get(url3).json()
            current_temperature = response_2.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response_2.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response_2.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response_2.get('main', {}).get('humidity')

            weather = response_2.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)

        else:
            current_temperature = response.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response.get('main', {}).get('humidity')

            weather = response.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)
        dados_json = json.dumps(output_list)
        x = x + 1

    return dados_json

@app.route('/sul')
def random_sul():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    sul = ['Maracaju', 'Rio Brilhante', 'Itaporã', 'douradina',  'jateí',
           'fátima do sul', 'deodápolis', 'Caarapó', 'Vicentina', 'glória de dourados',
           'Juti', 'Naviraí', 'itaquiraí', 'Iguatemi', 'Japorã', 'Eldorado', 'Mundo Novo',
           'Nova Andradina', 'antônio joão', 'Laguna Carapã', 'Aral Moreira', 'Amambai',
           'Coronel Sapucaia', 'Tacuru', 'Paranhos', 'Sete Quedas']

    cidades = random.sample(sul, 5)

    x = 0
    output_list = []
    while x < 5:
        city = cidades[x]
        url2 = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url2).json()

        if response.get('cod') != 200:
            municipio = [city.title()]
            municipios = pd.read_csv("municipios_rmc.csv")
            lat = municipios['latitude'].loc[municipios['nome'].isin(municipio)]
            lat = float(lat)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon)
            url3 = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID={API_KEY}'
            response_2 = requests.get(url3).json()
            current_temperature = response_2.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response_2.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response_2.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response_2.get('main', {}).get('humidity')

            weather = response_2.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)

        else:
            current_temperature = response.get('main', {}).get('temp')
            current_temperature_celsius = round(current_temperature - 273.15, 2)

            min_temperature = response.get('main', {}).get('temp_min')
            min_temperature_celsius = round(min_temperature - 273.15, 2)

            max_temperature = response.get('main', {}).get('temp_max')
            max_temperature_celsius = round(max_temperature - 273.15, 2)

            humidity = response.get('main', {}).get('humidity')

            weather = response.get('weather', {})

            df = pd.DataFrame(weather)
            new_dict = pd.DataFrame.to_dict(df)

            clima = json.dumps(new_dict['main'])
            clima = clima[6:len(clima) - 1]

            descricao = json.dumps(new_dict['description'])
            descricao = descricao[6:len(descricao) - 1]

            if clima == "\"Rain\"":
                mm = response.get('rain', {}).get('1h')
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'mm de chuva': mm,
                    'descricao': descricao
                }
            else:
                dados = {
                    'cidade': city.title(),
                    'temperatura': current_temperature_celsius,
                    'minima': min_temperature_celsius,
                    'maxima': max_temperature_celsius,
                    'umidade do ar': humidity,
                    'clima': clima,
                    'descricao': descricao
                }

            output_list.append(dados)
        dados_json = json.dumps(output_list)
        x = x + 1

    return dados_json


@app.route('/')
def index():
    return '<h1>TV Morena</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
