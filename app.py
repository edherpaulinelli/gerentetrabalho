from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Usando SQLite, você pode alterar para outro banco de dados se necessário
db = SQLAlchemy(app)

# Modelo para a tabela de opções
class Opcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opcao = db.Column(db.String(255), nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar_opcao', methods=['POST'])
def registrar_opcao():
    data = request.get_json()
    opcoes = data.get('opcoes', [])

    if opcoes:
        try:
            # Inserir opções no banco de dados
            for opcao_texto in opcoes:
                nova_opcao = Opcao(opcao=opcao_texto)
                db.session.add(nova_opcao)

            # Commit
            db.session.commit()

            return jsonify({'message': 'Opções registradas com sucesso!'})

        except Exception as e:
            return jsonify({'error': f'Erro ao salvar no banco de dados: {str(e)}'}), 500

    return jsonify({'error': 'Nenhuma opção fornecida para registro'}), 400

if __name__ == "__main__":
    app.run(debug=True)
