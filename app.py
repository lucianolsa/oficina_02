from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import select,extract
from datetime import timedelta,datetime
from dotenv import load_dotenv
from models import db_session, Usuario, Proprietario, Carro,Agendamento
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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
@login_required
def dashboard():
    # Renderiza tela com links para Produtos e Estoque e mostra current_user.nome (5.1.1)
    return render_template('dashboard.html')

@app.route('/carro', methods=['GET', 'POST'])
@login_required
def carro():
    termo = request.form.get('busca','')
    if termo:
        busca_carros = (select(Carro)
                         .where(Carro.placa.ilike(f'%{termo}%')))

    else:
        busca_carros = select(Carro)
    carros= db_session.execute(busca_carros).scalars().all()

    return render_template(
        'carros.html',
        carros=carros)


@app.route('/carro/novo', methods=['GET', 'POST'])
@login_required
def carro_novo():
    proprietarios = db_session.execute(
        select(Proprietario)
    ).scalars().all()

    if request.method == 'POST':
        modelo = request.form.get('modelo')
        placa = request.form.get('placa')
        proprietario_id = request.form.get('proprietario_id')

        try:
            carro = Carro(
                modelo=modelo,
                placa=placa.upper().strip(),
                proprietario_id=int(proprietario_id)
            )

            db_session.add(carro)
            db_session.commit()

            flash('Carro cadastrado com sucesso!', 'success')

            return redirect(url_for('carro_novo'))

        except Exception:
            db_session.rollback()
            flash('Erro ao cadastrar carro. Verifique a placa e o proprietário.', 'danger')

    return render_template(
        'carro_novo.html',
        proprietarios=proprietarios
    )

@app.route('/proprietario', methods=['GET', 'POST'])
@login_required
def proprietario():
    termo = request.form.get('busca','')
    if termo:
        busca_proprietarios = (select(Proprietario)
                         .where(Proprietario.nome.ilike(f'%{termo}%')))

    else:
        busca_proprietarios = select(Proprietario)
    proprietarios= db_session.execute(busca_proprietarios).scalars().all()

    return render_template(
        'proprietario.html',
        proprietarios=proprietarios)

@app.route('/proprietario/novo', methods=['GET', 'POST'])
@login_required
def proprietario_novo():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        cpf = request.form['cpf']

        # Validar CPF
        if not Proprietario.validar_formato_cpf(cpf):
            flash('CPF inválido!')
            return redirect(url_for('proprietario_novo'))
        try:
            novo = Proprietario(
                nome=nome,
                telefone=telefone,
                email=email
            )

            novo.set_cpf(cpf)

            db_session.add(novo)
            db_session.commit()

            flash('Proprietário cadastrado com sucesso!')

            return redirect(url_for('proprietario'))
        except Exception as e:
            db_session.rollback()
            flash("Erro ao cadastrar", 'danger')
            return redirect(url_for('proprietario_novo'))

    return render_template('proprietario_novo.html')

@app.route('/proprietario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def proprietario_editar(id):
    proprietario = db_session.get(Proprietario, id)
    if not proprietario:
        flash('Proprietário não encontrado!')
        return redirect(url_for('proprietario'))

    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')

    cpf = request.form.get('cpf')

    if request.method == 'POST':
        try:
            if nome != proprietario.nome:
                proprietario.nome = nome
            if telefone != proprietario.telefone:
                proprietario.telefone = telefone
            if email != proprietario.email:
                proprietario.email = email
            if cpf:
                proprietario.set_cpf(cpf)

            db_session.commit()

            flash('Proprietário atualizado com sucesso!')
            return redirect(url_for('proprietario'))
        except ValueError as e:
            flash(f"{e}")
            db_session.rollback()
            return redirect(url_for('proprietario_editar', id=id))

        except Exception as e:
            db_session.rollback()
            print(e)
            flash('Erro ao atualizar proprietário!')
            return redirect(url_for('proprietario_editar', id=id))

    return render_template(
        'proprietario_editar.html',
        proprietario=proprietario
    )

@app.route('/agendamentos', methods=['GET'])
@login_required
def agendamentos():
    agendamentos = db_session.execute(
        select(Agendamento).order_by(
            extract('day', Agendamento.data_hora).asc())
    ).scalars().all()
    print(agendamentos)

    return render_template('agendamentos.html', agendamentos=agendamentos)

@app.route('/agendamentos/atualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def agendamento_atualizar(id):
    agendamento = db_session.get(Agendamento, id)
    if not agendamento:
        flash('Agendamento não encontrado!')
        return redirect(url_for('agendamentos'))
    if request.method == 'POST':
        data_hora_html = request.form.get('data_hora')  # Ex: "2026-11-10T14:00"
        try:
            # 1. Convertemos a string do HTML num Objeto Datetime
            data_hora_obj = datetime.strptime(data_hora_html, '%Y-%m-%dT%H:%M')

            if data_hora_obj == agendamento.data_hora:
                flash("Mesmo horario de Agendamento")
                return redirect(url_for('agendamentos'))


            # 2. Regra de Negócio: Horário Comercial (08h às 18h)
            if data_hora_obj.hour < 8 or data_hora_obj.hour >= 18:
                flash("A oficina só funciona das 08:00 às 18:00.", "warning")
                return redirect(url_for('agendamentos'))

            # 3. Regra de Negócio: Horas Cheias
            if data_hora_obj.minute != 0:
                flash("Agendamentos apenas em horas exatas (Ex: 14:00).", "warning")
                return redirect(url_for('agendamentos'))

            # 4. REGRA DE CONFLITO (Agora buscando direto pelo objeto DateTime!)
            # O banco compara objetos de tempo de forma nativa e ultra rápida
            stmt_conflito = select(Agendamento).where(Agendamento.data_hora == data_hora_obj)
            horario_ocupado = db_session.execute(stmt_conflito).first()

            if horario_ocupado is not None:
                flash("Este horário já está reservado!", "danger")
                return redirect(url_for('agendamentos'))

            # 5. SALVAMENTO (Enviamos o objeto data_hora_obj direto)
            agendamento.data_hora = data_hora_obj
            db_session.commit()

            flash("Agendamento atualizado com sucesso!", "success")
            return redirect(url_for('agendamentos'))

        except ValueError:
            flash("Formato de data inválido.", "danger")
            return redirect(url_for('agendamentos'))
        except Exception as e:
            db_session.rollback()
            print(f"Erro: {e}")
            flash("Erro interno ao salvar.", "danger")
            return redirect(url_for('agendamentos'))



    return render_template('agendamento_atualizar.html', agendamento=agendamento)

@app.route('/agendamentos/novo', methods=['GET', 'POST'])
@login_required
def agendamento_novo():
    if request.method == 'POST':
        carro_id = request.form.get('carro_id')
        data_hora_html = request.form.get('data_hora')  # Ex: "2026-11-10T14:00"
        servico = request.form.get('servico')

        if not carro_id or not data_hora_html or not servico:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('novo_agendamento'))

        try:
            # 1. Convertemos a string do HTML num Objeto Datetime
            data_hora_obj = datetime.strptime(data_hora_html, '%Y-%m-%dT%H:%M')

            # 2. Regra de Negócio: Horário Comercial (08h às 18h)
            if data_hora_obj.hour < 8 or data_hora_obj.hour >= 18:
                flash("A oficina só funciona das 08:00 às 18:00.", "warning")
                return redirect(url_for('novo_agendamento'))

            # 3. Regra de Negócio: Horas Cheias
            if data_hora_obj.minute != 0:
                flash("Agendamentos apenas em horas exatas (Ex: 14:00).", "warning")
                return redirect(url_for('novo_agendamento'))

            # 4. REGRA DE CONFLITO (Agora buscando direto pelo objeto DateTime!)
            # O banco compara objetos de tempo de forma nativa e ultra rápida
            stmt_conflito = select(Agendamento).where(Agendamento.data_hora == data_hora_obj)
            horario_ocupado = db_session.execute(stmt_conflito).first()

            if horario_ocupado is not None:
                flash("Este horário já está reservado!", "danger")
                return redirect(url_for('agendamentos'))

            # 5. SALVAMENTO (Enviamos o objeto data_hora_obj direto)
            novo_agendamento = Agendamento(
                carro_id=carro_id,
                data_hora=data_hora_obj,  # Salvando como DateTime real
                servico=servico
            )

            db_session.add(novo_agendamento)
            db_session.commit()

            flash("Agendamento criado com sucesso!", "success")
            return redirect(url_for('agendamentos'))

        except ValueError:
            flash("Formato de data inválido.", "danger")
            return redirect(url_for('novo_agendamento'))
        except Exception as e:
            db_session.rollback()
            print(f"Erro: {e}")
            flash("Erro interno ao salvar.", "danger")
            return redirect(url_for('agendamento_novo'))
    # se get
    carros_disponiveis = db_session.execute(select(Carro)).scalars().all()
    return render_template('agendamento_novo.html', carros=carros_disponiveis)

if __name__ == '__main__':
    app.run(debug=True, port=5007, host='0.0.0.0')
