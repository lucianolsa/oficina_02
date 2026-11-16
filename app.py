from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import select
from datetime import timedelta

from models import db_session, Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

# Tempo máximo de login: 30 minutos
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Configuração do Flask-Login (Requisito 4 e 5)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Faça login para acessar o sistema."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = db_session.execute(select(Usuario).where(Usuario.email == email)).scalar()

        if usuario and usuario.check_password(senha):
            session.permanent = True
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            # Requisito 4.1: Informar motivo da falha
            flash('Falha na autenticação: E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Requisito 5.1.2
    return redirect(url_for('login'))

@app.route('/')

def dashboard():
    # Renderiza tela com links para Produtos e Estoque e mostra current_user.nome (5.1.1)
    return render_template('dashboard.html')

@app.route('/carro/novo', methods=['GET', 'POST'])

def carro_novo():
    return render_template('carro_novo.html')

@app.route('/proprietario', methods=['GET'])

def proprietario():
    return render_template('proprietario.html')

@app.route('/proprietario/novo', methods=['GET', 'POST'])

def proprietario_novo():
    return render_template('proprietario_novo.html')

@app.route('/agendamentos', methods=['GET'])

def agendamentos():
    return render_template('agendamentos.html')

@app.route('/agendamentos/novo', methods=['GET', 'POST'])

def agendamento_novo():
    return render_template('agendamento_novo.html')

if __name__ == '__main__':
    app.run(debug=True, port=5007, host='0.0.0.0')
