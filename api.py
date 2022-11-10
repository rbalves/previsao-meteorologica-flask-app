from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route("/")
def consulta():
    resposta = requests.get('https://apiprevmet3.inmet.gov.br/previsao/capitais/')
    previsoes = json.loads(resposta.content)
    capitais = list(previsoes.keys())
    return render_template('consulta.html', capitais=capitais)

@app.route("/consultar")
def consultar():
    resposta = requests.get('https://apiprevmet3.inmet.gov.br/previsao/capitais/')
    previsoes = json.loads(resposta.content)

    capital = request.args.get('capital')

    dados_capital = previsoes[capital]

    datas = list(dados_capital.keys())

    dia_atual = datas[0]
    dia_seguinte = datas[1]

    temperaturas_maximas_dia_atual = [
        dados_capital[dia_atual]['manha']['temp_max'],
        dados_capital[dia_atual]['tarde']['temp_max'],
        dados_capital[dia_atual]['noite']['temp_max']
    ]

    temperaturas_maximas_dia_seguintes = [
        dados_capital[dia_seguinte]['manha']['temp_max'],
        dados_capital[dia_seguinte]['tarde']['temp_max'],
        dados_capital[dia_seguinte]['noite']['temp_max']
    ]

    temperaturas_minimas_dia_seguintes = [
        dados_capital[dia_seguinte]['manha']['temp_min'],
        dados_capital[dia_seguinte]['tarde']['temp_min'],
        dados_capital[dia_seguinte]['noite']['temp_min']
    ]

    dados = {
        'capital': capital,
        'temperaturas_maxima_dia_atual': max(temperaturas_maximas_dia_atual),
        'temperaturas_maxima_dia_seguinte': max(temperaturas_maximas_dia_seguintes),
        'temperaturas_minima_dia_seguinte': min(temperaturas_minimas_dia_seguintes)
    }

    return render_template('dados.html', dados=dados)