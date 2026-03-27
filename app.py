from flask import Flask, request, redirect, session, render_template
from models import db, Usuario, Lancamento
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

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

    lancamentos = Lancamento.query.filter_by(
        usuario_id=session["user_id"]
    ).all()

    total_receitas = 0
    total_despesas = 0

    for l in lancamentos:
        if l.tipo == "R":
            total_receitas += l.valor
        else:
            total_despesas += l.valor

    saldo = total_receitas - total_despesas

    return render_template(
        "dashboard.html",
        lancamentos=lancamentos,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo
    )


@app.route("/add", methods=["POST"])
def add():
    novo = Lancamento(
        descricao=request.form["descricao"],
        valor=request.form["valor"],
        tipo=request.form["tipo"],
        usuario_id=session["user_id"]
    )

    db.session.add(novo)
    db.session.commit()

    return redirect("/dashboard")


@app.route("/delete/<int:id>")
def delete(id):
    lanc = Lancamento.query.get(id)
    db.session.delete(lanc)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    lanc = Lancamento.query.get(id)

    if request.method == "POST":
        lanc.descricao = request.form["descricao"]
        lanc.valor = request.form["valor"]
        lanc.tipo = request.form["tipo"]

        db.session.commit()
        return redirect("/dashboard")

    return render_template("edit.html", lanc=lanc)


app.run(debug=True)