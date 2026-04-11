from models import Lancamento
from datetime import datetime

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