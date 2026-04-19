from flask import current_app, redirect, render_template, request, send_file, session
from app.models import db, Usuario, Lancamento
from app.services.emailServices import enviar_email
from app.services.services import (
    atualizar_lancamento,
    calcular_totais,
    criar_lancamento,
    filtrar_lancamentos,
)
from app.services.servicesRelatorio import gerar_pdf_lancamentos


def init_routes(app):

    # ------------------------------
    # Rotas da aplicação
    # ------------------------------
    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = Usuario.query.filter_by(
                login=request.form["login"], senha=request.form["senha"]
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
        status = request.args.get("status")

        lancamentos = filtrar_lancamentos(
            session["user_id"], data_inicio, data_fim, status
        )

        total_receitas, total_despesas, saldo = calcular_totais(lancamentos)

        return render_template(
            "dashboard.html",
            lancamentos=lancamentos,
            total_receitas=total_receitas,
            total_despesas=total_despesas,
            saldo=saldo,
        )

    @app.route("/add", methods=["POST"])
    def add():
        if "user_id" not in session:
            return redirect("/")

        try:
            novo = criar_lancamento(request.form, session["user_id"])

            db.session.add(novo)
            db.session.commit()

            user = db.session.get(Usuario, session["user_id"])

            if user and user.email and not current_app.config.get("TESTING"):
                enviar_email(
                    user.email,
                    "Novo lançamento criado",
                    f"Lançamento '{novo.descricao}' no valor de R$ {novo.valor} foi criado.",
                )

        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar lançamento: {e}")

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
        if "user_id" not in session:
            return redirect("/")

        lanc = db.session.get(Lancamento, id)

        if not lanc:
            return redirect("/dashboard")

        if request.method == "POST":
            try:
                atualizar_lancamento(lanc, request.form)
                db.session.commit()

                user = db.session.get(Usuario, session["user_id"])

                if user and user.email and not current_app.config.get("TESTING"):
                    enviar_email(
                        user.email,
                        "Lançamento atualizado",
                        f"Lançamento '{lanc.descricao}' foi atualizado com sucesso.",
                    )

            except Exception as e:
                db.session.rollback()
                print(f"Erro ao atualizar lançamento: {e}")

            return redirect("/dashboard")

        return render_template("edit.html", lanc=lanc)

    @app.route("/relatorio")
    def relatorio():
        if "user_id" not in session:
            return redirect("/")

        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        status = request.args.get("status")

        lancamentos = filtrar_lancamentos(
            session["user_id"], data_inicio, data_fim, status
        )

        total_receitas, total_despesas, saldo = calcular_totais(lancamentos)

        pdf = gerar_pdf_lancamentos(lancamentos, total_receitas, total_despesas, saldo)

        return send_file(
            pdf,
            as_attachment=True,
            download_name="relatorio.pdf",
            mimetype="application/pdf",
        )
