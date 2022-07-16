import random
from flask import Flask, Response, request
import json
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    args = request.args
    if'combinacoes' not in args.keys() or 'dezenas' not in args.keys():
        return 'Parâmetros inválidos'
    combinacoes = int(args.get('combinacoes'))
    dezenas = int(args.get('dezenas'))
    
    validar = validacao(dezenas)
    if type(validar['key']) == str: 
      return validar['key']

    lista_jogos = {}

    for i in range(1, combinacoes + 1):
        lista_numeros = []
        for _ in range(0, dezenas):
          valor = random.randint(1, 25)
          while valor in lista_numeros:
            valor = random.randint(1, 25)
          lista_numeros.append(valor)
          lista_numeros.sort()
          lista_jogos[i] = lista_numeros
    
    print(lista_jogos)
    return Response(json.dumps(lista_jogos), mimetype='application/json')

def validacao(valor):
  if valor > 15: 
    return {"key":"Valor inválido. Por favor, digite um valor entre 1 e 15"} 
  return {"key": False}

@app.route('/resultados', methods=['GET'])  
def obterResultadoMegaSena( ):
    try:
        req = requests.get( "https://www.loteriaseresultados.com.br/megasena/resultado/2500")
        soup = BeautifulSoup( req.content, "html.parser" )
        dezenas = [ int(dezena.text) for dezena in soup.findAll( "span", class_="white--text font-weight-bold" ) ]
        return { "Concurso" : "2500", "DezenasSorteadas" : dezenas}
    except:
        return None

print( obterResultadoMegaSena() )

@app.route('/resultados-concursos', methods=['GET'])  
def obterResultadoConcursosMegaSena( ):
    try:
        req = requests.get( "https://www.loteriaseresultados.com.br/megasena/concurso")
        soup = BeautifulSoup( req.content, "html.parser" )
        concurso = [int(concurso.text) for concurso in soup.findAll( "td", class_="text-center" )]
        dezenas = [ int(dezena.text) for dezena in soup.findAll( "td", class_="text-center" ) ]
        return { "Concurso" : concurso, "DezenasSorteadas" : dezenas}
    except:
        return None

print( obterResultadoConcursosMegaSena() )

if __name__ == '__main__':
    app.run(debug=True)