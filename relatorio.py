
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

prompt = """Gere um relatório diário sobre 5 frases em inglês dentre os níveis B2 a C1, 
explicando o significado de cada frase e como usar em outros contextos. Quando for dar 
definição de palavras use a Dictionary. Evite falar dos mesmos tópicos e temas de gramática.

1 texto em inglês de até 1000 palavras. Temas: desenvolvimento pessoal, produtividade, 
comportamento humano e outros temas semelhantes. Sempre traga um insight interessante 
e/ou desconhecido, para me informar e treinar meu inglês.

Um fato aleatório sobre conhecimentos gerais."""

response = model.generate_content(prompt)
relatorio = response.text

remetente = os.environ["EMAIL_FROM"]
senha = os.environ["EMAIL_APP_PASSWORD"]
destinatario = os.environ["EMAIL_TO"]

msg = MIMEMultipart()
msg["From"] = remetente
msg["To"] = destinatario
msg["Subject"] = f"Relatório Diário - {datetime.now().strftime('%d/%m/%Y')}"
msg.attach(MIMEText(relatorio, "plain", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(remetente, senha)
    server.sendmail(remetente, destinatario, msg.as_string())

print("Relatório enviado!")
