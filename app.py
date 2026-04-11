from flask import Flask, request, redirect, session, render_template
from models import db, Usuario, Lancamento
from services import filtrar_lancamentos, calcular_totais, criar_lancamento, atualizar_lancamento
import config


def create_app(test_config=None):
    app = Flask(__name__)

    # Configuração de teste ou produção
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(config)

    db.init_app(app)

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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)