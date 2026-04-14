import smtplib
from email.mime.text import MIMEText
import os
from flask import current_app

def enviar_email(destinatario, assunto, mensagem):
    remetente = current_app.config["EMAIL_USER"]
    senha = current_app.config["EMAIL_PASSWORD"]

    if not remetente or not senha:
        raise ValueError("Configuração de e-mail não encontrada no .env")

    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remetente, senha)
        server.send_message(msg)