from flask import Flask, request
import pandas as pd
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


@app.route('/cidades')
def random_cities():
    API_KEY = '3bc9b1c2c07e4f4dad648c37e3039f3a'

    campogrande = ['Corguinho', 'Bandeirantes', 'Rochedo', 'Ribas do Rio Pardo', 'Terenos',
                   'Jaraguari', 'Dois Irmãos do Buriti', 'Sidrolândia', 'Nova Alvorada do Sul']

    grandedourados = ['Maracaju', 'Rio Brilhante', 'Itaporã', 'Douradina', 'Dourados', 'Jateí',
                      'Fátima do Sul', 'Deodápolis', 'Caarapó', 'Vicentina', 'Glória de Dourados']

    bolsao = ['Juti', 'Naviraí', 'Itaquiraí', 'Iguatemi', 'Japorã', 'Eldorado', 'Mundo Novo']

    conesul = ['Chapadão do Sul', 'Cassilândia', 'Paraíso das Águas', 'Inocência', 'Paranaíba',
               'Aparecida do Taboado', 'Água Clara', 'Três Lagoas', 'Santa Rita do Pardo', 'Brasilândia']

    pantanal = ['Corumbá', 'Ladário', 'Miranda', 'Aquidauana', 'Anastácio']

    leste = ['Bataguassu', 'Nova Andradina', 'Angélica', 'Ivinhema', 'Novo Horizonte do Sul',
             'Anaurilândia', 'Bataiporã', 'Taquarussu']

    norte = ['Sonora', 'Pedro Gomes', 'Coxim', 'Rio Verde de Mato Grosso', 'São Gabriel do Oeste',
             'Rio Negro', 'Camapuã', 'Alcinópolis', 'Costa Rica', 'Figueirão']

    sudoeste = ['Porto Murtinho', 'Bonito', 'Bodoquena', 'Caracol', 'Jardim', 'Bela Vista', 'Nioaque',
                'Guia Lopes da Laguna']

    sulfronteira = ['Antônio João', 'Ponta Porã', 'Laguna Carapã', 'Aral Moreira', 'Amambai',
                    'Coronel Sapucaia', 'Taçuru', 'Paranhos', 'Sete Quedas']

    regioes = ['campogrande', 'grandedourados', 'bolsao', 'conesul', 'pantanal', 'leste',
               'norte', 'sudoeste', 'sulfronteira']

    regiao = random.sample(regioes, 1)

    for i in regiao:
        if i == 'campogrande':
            cidades = random.sample(campogrande, 5)
        elif i == 'grandedourados':
            cidades = random.sample(grandedourados, 5)
        elif i == 'bolsao':
            cidades = random.sample(bolsao, 5)
        elif i == 'conesul':
            cidades = random.sample(conesul, 5)
        elif i == 'pantanal':
            cidades = random.sample(pantanal, 5)
        elif i == 'leste':
            cidades = random.sample(leste, 5)
        elif i == 'norte':
            cidades = random.sample(norte, 5)
        elif i == 'sudoeste':
            cidades = random.sample(sudoeste, 5)
        else:
            cidades = random.sample(sulfronteira, 5)

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
            lat = float(lat.values)
            lon = municipios['longitude'].loc[municipios['nome'].isin(municipio)]
            lon = float(lon.values)
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
