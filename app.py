from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, render_template_string
import flask
import os
import random
import io
import sys
import traceback
import threading
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from challenges import CHALLENGES, get_topics_by_level, get_challenges_filtered, get_challenge_by_id, get_points, get_challenges_by_topic

# ----------------- FLASK SETUP ------------------
app = Flask(__name__)
app.secret_key = "super_secret_key_CSA"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email settings
app.config['MAIL_SERVER'] = 'smtp.seuprovedor.com'  # Ex: smtp.gmail.com
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'julioamancio2014@gmail.com'
app.config['MAIL_PASSWORD'] = 'bbkdgkdekincbdlq'
app.config['MAIL_DEFAULT_SENDER'] = 'julioamancio2014@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

print("VERSÃO DO FLASK:", flask.__version__)
print("MODULO FLASK:", flask)
print("CAMINHO DO MODULO FLASK:", flask.__file__)

# ----------------- MODELOS ------------------
class Aluno(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    turma = db.Column(db.String(20), nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

class Progresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    desafio_id = db.Column(db.String(50), nullable=False)
    tentativas = db.Column(db.Integer, default=0)
    nota = db.Column(db.Integer, default=0)
    last_code = db.Column(db.Text)

class EmailRelatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    assunto = db.Column(db.String(100), nullable=False)
    enviado_em = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Aluno.query.get(int(user_id))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        progresso = Progresso.query.filter_by(aluno_id=current_user.id).all()
        g.pontos = sum(p.nota for p in progresso)
        g.medalhas_ouro, g.medalhas_prata, g.medalhas_bronze = calcular_medalhas(current_user.id)
    else:
        g.pontos = 0
        g.medalhas_ouro, g.medalhas_prata, g.medalhas_bronze = 0, 0, 0

# ----------------- ROTAS ------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        turma = request.form["turma"]
        senha = request.form["senha"]
        if Aluno.query.filter_by(email=email).first():
            flash("Email já cadastrado!")
            return redirect(url_for("cadastro"))
        aluno = Aluno(nome=nome, email=email, turma=turma, senha_hash=generate_password_hash(senha))
        db.session.add(aluno)
        db.session.commit()
        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        aluno = Aluno.query.filter_by(email=email).first()
        if aluno and check_password_hash(aluno.senha_hash, senha):
            login_user(aluno)
            return redirect(url_for("dashboard"))
        else:
            flash("Email ou senha incorretos.")
    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.")
    return redirect(url_for("login"))

@app.route("/select", methods=["GET", "POST"])
@login_required
def select():
    levels = list(CHALLENGES.keys())
    selected_level = request.form.get("level") if request.method == "POST" else levels[0]
    topics = get_topics_by_level(selected_level)
    progresso = Progresso.query.filter_by(aluno_id=current_user.id).all()
    pontos = sum(p.nota for p in progresso)
    if request.method == "POST":
        level = request.form.get("level")
        topic = request.form.get("topic")
        progresso_ids = [p.desafio_id for p in progresso]
        challenges = get_challenges_filtered(level, topic, exclude_ids=progresso_ids)
        if not challenges:
            return render_template("select.html", levels=levels, topics=topics, selected_level=level, selected_topic=topic, no_challenge=True, pontos=pontos)
        challenge = random.choice(challenges)
        return redirect(url_for("challenge", cid=challenge["id"]))
    return render_template("select.html", levels=levels, topics=topics, selected_level=selected_level, selected_topic=None, no_challenge=False, pontos=pontos)

@app.route("/get_topics/<level>")
@login_required
def get_topics(level):
    return jsonify(get_topics_by_level(level))

@app.route("/challenge/<cid>")
@login_required
def challenge(cid):
    challenge = get_challenge_by_id(cid)
    if not challenge:
        flash("Desafio não encontrado.")
        return redirect(url_for("select"))
    progresso = Progresso.query.filter_by(aluno_id=current_user.id, desafio_id=cid).first()
    last_code = progresso.last_code if progresso else ""
    return render_template("challenge.html", challenge=challenge, show_solution=last_code, progresso=progresso)

@app.route("/run_code", methods=["POST"])
@login_required
def run_code():
    code = request.form.get("code", "")
    input_data = request.form.get("input_data", "")
    cid = request.form.get("cid")
    output, error = exec_student_code(code, input_data)
    sucesso = not error
    pontos = None
    desbloqueou = False
    progresso = Progresso.query.filter_by(aluno_id=current_user.id, desafio_id=cid).first()
    pontuou = False
    acertou_primeira = False
    acertou_segunda = False

    if sucesso:
        if not progresso:
            progresso = Progresso(aluno_id=current_user.id, desafio_id=cid, tentativas=1, nota=get_points(get_challenge_by_id(cid)), last_code=code)
            db.session.add(progresso)
            pontuou = True
            acertou_primeira = True
        else:
            if progresso.nota == 0:
                progresso.nota = get_points(get_challenge_by_id(cid))
                pontuou = True
                if progresso.tentativas == 1:
                    acertou_segunda = True
            progresso.last_code = code
            progresso.tentativas += 1
        db.session.commit()
        pontos = sum(p.nota for p in Progresso.query.filter_by(aluno_id=current_user.id).all())
        desbloqueou = pontuou
    else:
        if progresso:
            progresso.last_code = code
            progresso.tentativas += 1
            db.session.commit()
        pontos = sum(p.nota for p in Progresso.query.filter_by(aluno_id=current_user.id).all())

    if sucesso and pontuou:
        challenge = get_challenge_by_id(cid)
        assunto = challenge['topic']
        desafios_do_assunto = get_challenges_by_topic(assunto)
        ids_do_assunto = set(d['id'] for d in desafios_do_assunto)
        progresso_ids = set(p.desafio_id for p in Progresso.query.filter_by(aluno_id=current_user.id).all() if p.nota > 0)
        ja_enviado = EmailRelatorio.query.filter_by(aluno_id=current_user.id, assunto=assunto).first()
        if ids_do_assunto.issubset(progresso_ids) and not ja_enviado:
            desafios_pontuados = [d for d in desafios_do_assunto if d['id'] in progresso_ids]
            pontos_assunto = sum(d['points'] for d in desafios_pontuados)
            send_subject_report(current_user, assunto, desafios_pontuados, pontos_assunto)
            db.session.add(EmailRelatorio(aluno_id=current_user.id, assunto=assunto))
            db.session.commit()

    g.medalhas_ouro, g.medalhas_prata, g.medalhas_bronze = calcular_medalhas(current_user.id)

    return jsonify({
        "output": output,
        "error": error,
        "sucesso": sucesso,
        "pontos": pontos,
        "desbloqueou": desbloqueou,
        "medalhas_ouro": g.medalhas_ouro,
        "medalhas_prata": g.medalhas_prata,
        "medalhas_bronze": g.medalhas_bronze
    })

@app.route("/apostilas")
@login_required
def apostilas():
    return render_template("apostilas.html")

@app.route("/historico")
@login_required
def historico():
    progresso = Progresso.query.filter_by(aluno_id=current_user.id).all()
    desafios = [(get_challenge_by_id(p.desafio_id), p) for p in progresso]
    return render_template("historico.html", desafios=desafios, aluno=current_user)

# ----------------- FUNÇÕES AUXILIARES ------------------
def calcular_medalhas(aluno_id):
    progresso = Progresso.query.filter_by(aluno_id=aluno_id).all()
    ouro = prata = bronze = 0
    for p in progresso:
        if p.nota > 0:
            if p.tentativas == 1:
                ouro += 1
            elif p.tentativas == 2:
                prata += 1
            else:
                bronze += 1
    return ouro, prata, bronze

def exec_student_code(code, input_data=""):
    output = ""
    error = ""
    def run():
        nonlocal output, error
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        sys_stdout, sys_stderr, sys_stdin = sys.stdout, sys.stderr, sys.stdin
        sys.stdout = buf_out
        sys.stderr = buf_err
        sys.stdin = io.StringIO(input_data)
        try:
            exec(code, {})
        except EOFError:
            error = "[ERRO] Faltou entrada para o(s) comando(s) input()."
        except Exception:
            error = buf_err.getvalue() + traceback.format_exc(limit=2)
        finally:
            output = buf_out.getvalue()
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr
            sys.stdin = sys_stdin

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    t.join(3)
    if t.is_alive():
        return "Tempo excedido ou loop infinito.", "Timeout"
    return output, error

def send_subject_report(aluno, subject, desafios, pontos_total):
    try:
        import pytz
        datahora = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
    except Exception:
        datahora = datetime.now().strftime('%d/%m/%Y %H:%M')

    html = render_template_string("""
    <h2>Relatório de conclusão de assunto</h2>
    <b>Aluno:</b> {{ aluno.nome }}<br>
    <b>Turma:</b> {{ aluno.turma }}<br>
    <b>Email do aluno:</b> {{ aluno.email }}<br>
    <b>Assunto:</b> {{ subject }}<br>
    <b>Total de pontos no assunto:</b> {{ pontos_total }}<br>
    <b>Data/hora:</b> {{ datahora }}<br>
    <hr>
    <ul>
    {% for d in desafios %}
        <li><b>{{ d['topic'] }}</b> - {{ d['description']|safe }} <br>
        <b>Pontuado:</b> {{ d['points'] }} ponto(s)</li>
    {% endfor %}
    </ul>
    """, aluno=aluno, subject=subject, desafios=desafios, pontos_total=pontos_total, datahora=datahora)

    msg = Message(
        subject=f"[Relatório] {aluno.nome} finalizou o assunto {subject}",
        recipients=['julioamancio2014@gmail.com', aluno.email],
        html=html
    )
    mail.send(msg)

# ----------------- INICIALIZAÇÃO DO BANCO ------------------
def inicializa_banco():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    inicializa_banco()
    app.run(host="0.0.0.0", port=5000, debug=True)
elif os.environ.get("RENDER") == "true" or "RENDER_EXTERNAL_HOSTNAME" in os.environ:
    inicializa_banco()
