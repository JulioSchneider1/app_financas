from app.models import Lancamento
from datetime import datetime, date
from sqlalchemy import func

# ==============================
# HELPERS
# ==============================


def parse_data(data):
    if not data:
        return None

    if isinstance(data, datetime):
        return data.date()

    if isinstance(data, date):
        return data

    if isinstance(data, str):
        data = data.strip()
        if not data:
            return None
        try:
            return datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            return None

    return None


def parse_status(status):
    """Converte status de string para boolean"""
    if status is None or status == "":
        return None

    if isinstance(status, bool):
        return status

    if isinstance(status, str):
        return True if status == "on" else False

    return None


# ==============================
# FUNÇÕES DE NEGÓCIO
# ==============================


def filtrar_lancamentos(user_id, data_inicio=None, data_fim=None, status=None):
    query = Lancamento.query.filter_by(usuario_id=user_id)

    data_inicio = parse_data(data_inicio)
    data_fim = parse_data(data_fim)

    if data_inicio:
        query = query.filter(func.date(Lancamento.data) >= data_inicio)

    if data_fim:
        query = query.filter(func.date(Lancamento.data) <= data_fim)

    if status is not None and status != "":
        if isinstance(status, str):
            if status == "on":
                status = True
            elif status == "off":
                status = False
            else:
                status = None

        if status is not None:
            query = query.filter(Lancamento.status == status)

    return query.all()


def calcular_totais(lancamentos):
    total_receitas = 0
    total_despesas = 0

    for lanc in lancamentos:
        if lanc.status:  # só considera efetuados
            if lanc.tipo == "R":
                total_receitas += lanc.valor
            else:
                total_despesas += lanc.valor

    saldo = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo


def criar_lancamento(form, user_id):
    data = parse_data(form.get("data"))
    status = parse_status(form.get("status"))

    return Lancamento(
        descricao=form["descricao"],
        valor=form["valor"],
        tipo=form["tipo"],
        usuario_id=user_id,
        data=data if data else datetime.today(),
        status=status if status is not None else False,
    )


def atualizar_lancamento(lanc, form):
    lanc.descricao = form["descricao"]
    lanc.valor = form["valor"]
    lanc.tipo = form["tipo"]

    data = parse_data(form.get("data"))
    status = parse_status(form.get("status"))

    if data:
        lanc.data = data

    if status is not None:
        lanc.status = status

    return lanc
