from flask import Flask, request, redirect, session, render_template
from models import db, Usuario, Lancamento
import config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

# ==============================
# FUNÇÕES DE NEGÓCIO
# ==============================

def filtrar_lancamentos(user_id, data_inicio=None, data_fim=None):
    query = Lancamento.query.filter_by(usuario_id=user_id)

    if data_inicio:
        query = query.filter(Lancamento.data >= data_inicio)

    if data_fim:
        query = query.filter(Lancamento.data <= data_fim)

    return query.all()


def calcular_totais(lancamentos):
    total_receitas = 0
    total_despesas = 0

    for l in lancamentos:
        if l.status:
            if l.tipo == "R":
                total_receitas += l.valor
            else:
                total_despesas += l.valor

    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo


def criar_lancamento(form, user_id):
    data = form.get("data")
    status = form.get("status")

    return Lancamento(
        descricao=form["descricao"],
        valor=form["valor"],
        tipo=form["tipo"],
        usuario_id=user_id,
        data=datetime.strptime(data, "%Y-%m-%d") if data else datetime.today(),
        status=True if status == "on" else False
    )


def atualizar_lancamento(lanc, form):
    lanc.descricao = form["descricao"]
    lanc.valor = form["valor"]
    lanc.tipo = form["tipo"]

    data = form.get("data")
    status = form.get("status")

    lanc.data = datetime.strptime(data, "%Y-%m-%d") if data else lanc.data
    lanc.status = True if status == "on" else False

    return lanc


# ==============================
# ROTAS
# ==============================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(
            login=request.form["login"],
            senha=request.form["senha"]
        ).first()

        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    lancamentos = filtrar_lancamentos(
        session["user_id"],
        data_inicio,
        data_fim
    )

    total_receitas, total_despesas, saldo = calcular_totais(lancamentos)

    return render_template(
        "dashboard.html",
        lancamentos=lancamentos,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo
    )


@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/")

    novo = criar_lancamento(request.form, session["user_id"])

    db.session.add(novo)
    db.session.commit()

    return redirect("/dashboard")


@app.route("/delete/<int:id>")
def delete(id):
    lanc = db.session.get(Lancamento, id)

    if lanc:
        db.session.delete(lanc)
        db.session.commit()

    return redirect("/dashboard")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    lanc = db.session.get(Lancamento, id)

    if request.method == "POST":
        atualizar_lancamento(lanc, request.form)

        db.session.commit()
        return redirect("/dashboard")

    return render_template("edit.html", lanc=lanc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)