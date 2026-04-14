from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def gerar_pdf_lancamentos(lancamentos, total_receitas=0, total_despesas=0, saldo=0):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    # ==============================
    # TÍTULO
    # ==============================
    elements.append(Paragraph("Relatório de Lançamentos", styles["Title"]))
    elements.append(Spacer(1, 12))

    # ==============================
    # TABELA DE DADOS
    # ==============================
    data = [
        ["Descrição", "Valor", "Tipo", "Data", "Status"]
    ]

    for l in lancamentos:
        data.append([
            l.descricao,
            f"R$ {float(l.valor):.2f}",
            "Receita" if l.tipo == "R" else "Despesa",
            l.data.strftime("%d/%m/%Y") if l.data else "-",
            "Efetuado" if l.status else "Pendente"
        ])

    tabela = Table(data, repeatRows=1)

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("ALIGN", (1, 1), (-1, -1), "CENTER"),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(tabela)
    elements.append(Spacer(1, 20))

    # ==============================
    # RESUMO FINANCEIRO
    # ==============================
    resumo = [
        ["Total Receitas", f"R$ {total_receitas:.2f}"],
        ["Total Despesas", f"R$ {total_despesas:.2f}"],
        ["Saldo", f"R$ {saldo:.2f}"],
    ]

    tabela_resumo = Table(resumo, colWidths=[200, 150])

    tabela_resumo.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))

    elements.append(Paragraph("Resumo", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(tabela_resumo)

    # ==============================
    # BUILD DO PDF
    # ==============================
    doc.build(elements)

    buffer.seek(0)
    return buffer