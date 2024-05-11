from flask import Flask, request, jsonify
import nltk # Importar biblioteca NLTK para processamento de texto

app = Flask(__name__)

@app.route('/gerar-vaga', methods=['POST'])
def gerar_vaga():
    # Receber dados do chat
    dados = request.get_json()
    empresa = dados['empresa']
    cargo = dados['cargo']
    requisitos = dados['requisitos']
    faixaSalarial = dados['faixaSalarial']
    tipoContrato = dados['tipoContrato']

    # Gerar resumo da empresa (usando NLTK)
    resumoEmpresa = nltk.sent_tokenize(empresa)[0] # Exemplo simples

    # Formatar texto
    textoFormatado = f"""VAGA: {cargo}

Sobre a empresa:
{resumoEmpresa} ({empresa})

Requisitos:
{requisitos}

Faixa Salarial: {faixaSalarial}

Tipo de Contrato: {tipoContrato}"""

    # Criar e salvar arquivo
    with open('vaga.txt', 'w') as f:
        f.write(textoFormatado)

    # Retornar resposta
    return jsonify({'sucesso': True})

if __name__ == '__main__':
    app.run(debug=True)
