from flask import Flask, render_template, request
import google.generativeai as genai
from markupsafe import Markup

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyC2F7mJg7fyuQ1H-GwmuoTnLJnJ1bd35AM' # Substitua 'SUA_API_KEY' pela sua API KEY
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    'candidate_count': 1,
    'temperature': 0.5,
}

safety_settings = {
    'HARASSMENT': 'BLOCK_NONE',
    'HATE': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE',
}

model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                              generation_config=generation_config,
                              safety_settings=safety_settings,)
chat = model.start_chat(history=[])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_template", methods=['POST'])
def generate_template():
    empresa = request.form['empresa']
    cargo = request.form['cargo']
    salario = request.form['salario']
    tipo_contrato = request.form['tipo_contrato']

     # Gerar prompt para o Gemini
    prompt_template = f"""
    Crie um template de vaga de emprego **em HTML** para a empresa {empresa} para a posição de {cargo}, com salário de {salario} e tipo de contrato {tipo_contrato}. 

    Use a seguinte estrutura HTML:

    
    Título da vaga: [Título da vaga]
    
    Descrição da empresa: [Descrição da empresa]
    
    Descrição da vaga: [Descrição da vaga]
    
    Responsabilidades: [Responsabilidades]
    
    Requisitos: [Requisitos]
    
    Benefícios: [Benefícios]
    
    Informações adicionais: [Informações adicionais]
    

    Substitua os campos entre colchetes ([]) pelas informações correspondentes.
    """

    # Obter requisitos mínimos para o cargo
    requisitos_prompt = f"Quais os requisitos mínimos para ser {cargo} no Brasil?"
    requisitos_response = chat.send_message(requisitos_prompt)
    requisitos = requisitos_response.text

    # Gerar template da vaga com o Gemini
    template_response = chat.send_message(prompt_template)
    template = template_response.text

    # Adicionar os requisitos mínimos na seção "Requisitos" do template
    template = template.replace("[Requisitos]", f"[Requisitos]\n{requisitos}")

    # Renderizar o HTML gerado pelo Gemini
    template = Markup(template)

    return render_template("index.html", 
                           empresa=empresa, 
                           cargo=cargo, 
                           salario=salario, 
                           tipo_contrato=tipo_contrato,
                           template=template)

if __name__ == "__main__":
    app.run(debug=True)