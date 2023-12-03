# Importando as bibliotecas necessárias
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from reportlab.pdfgen import canvas

# Configuração do Flask e do SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definindo o modelo de dados para a tabela 'Atividade'
class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.String(20), nullable=False)

# Rotas para a aplicação
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_opcao', methods=['POST'])
def registrar_opcao():
    data = request.get_json()

    # Criando uma nova atividade com a descrição da opção e uma data (substituir pela data real)
    atividade = Atividade(descricao=data['opcoes'][0], data='2023-12-03')
    db.session.add(atividade)
    db.session.commit()

    return jsonify({'message': 'Atividade registrada com sucesso!'})

@app.route('/relatorio', methods=['GET'])
def relatorio():
    filtro = request.args.get('filtro')

    # Lógica para obter dados do banco de dados
    atividades = Atividade.query.all()

    # Montar o conteúdo do relatório com base nos dados do banco de dados
    content = "Relatório Personalizado\n\n"
    content += f"Relatório para filtro: {filtro}\n\n"
    content += "Atividades registradas:\n"

    for atividade in atividades:
        content += f"- Descrição: {atividade.descricao}, Data: {atividade.data}\n"

    # Geração do PDF
    generate_pdf(content)

    return jsonify({'message': f'Relatório gerado com sucesso para filtro: {filtro}'})

# Função para gerar o PDF
def generate_pdf(content):
    filename = "relatorio.pdf"
    document_title = "Relatório Personalizado"

    # Configuração do PDF
    pdf = canvas.Canvas(filename)
    pdf.setTitle(document_title)
    pdf.drawString(100, 800, document_title)
    pdf.drawString(100, 780, content)

    # Salvar o PDF
    pdf.save()

# Inicialização da aplicação Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()

