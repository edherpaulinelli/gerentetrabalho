from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openpyxl import Workbook
from openpyxl.styles import Alignment
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

    atividade = Atividade(descricao=data['opcoes'][0], data='2023-12-03')  # Substitua '2023-12-03' pela data real
    db.session.add(atividade)
    db.session.commit()

    return jsonify({'message': 'Atividade registrada com sucesso!'})

@app.route('/relatorio', methods=['GET'])
def relatorio():
    filtro = request.args.get('filtro')

    # Lógica para gerar o relatório com base no filtro
    if filtro == 'dia':
        # Exemplo simples: obter todas as atividades do banco de dados
        atividades = Atividade.query.all()
        # Geração do XLSX
        generate_xlsx(atividades, filtro)
        return jsonify({'message': f'Relatório gerado com sucesso para filtro: {filtro}'})
    if filtro == 'semana':
        # Exemplo simples: obter todas as atividades do banco de dados
        atividades = Atividade.query.all()
        # Geração do XLSX
        generate_xlsx(atividades, filtro)
        return jsonify({'message': f'Relatório gerado com sucesso para filtro: {filtro}'})
    if filtro == 'mes':
        # Exemplo simples: obter todas as atividades do banco de dados
        atividades = Atividade.query.all()
        # Geração do XLSX
        generate_xlsx(atividades, filtro)
        return jsonify({'message': f'Relatório gerado com sucesso para filtro: {filtro}'})
    if filtro == 'ano':
        # Exemplo simples: obter todas as atividades do banco de dados
        atividades = Atividade.query.all()
        # Geração do XLSX
        generate_xlsx(atividades, filtro)
        return jsonify({'message': f'Relatório gerado com sucesso para filtro: {filtro}'})

    return jsonify({'error': 'Filtro não suportado'})

def generate_xlsx(atividades, filtro):
    filename = f"relatorio_{filtro}.xlsx"
    document_title = "Relatório Atividades"

    wb = Workbook()
    ws = wb.active
    ws.title = document_title

    # Adicionar título
    ws['A1'] = document_title
    ws['A2'] = ''

    # Adicionar dados
    for i, atividade in enumerate(atividades, start=3):
        ws[f'A{i}'] = f"Atividade: {atividade.descricao}"
        ws[f'B{i}'] = f"Data: {atividade.data}"
        ws[f'C{i}'] = ''  # Linha em branco entre atividades

    # Ajustar alinhamento
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)

    # Adicionar timestamp ao nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"{filename[:-5]}_{timestamp}.xlsx"

    # Salvar o XLSX
    wb.save(filename_with_timestamp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

