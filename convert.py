import io

import pandas as pd
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Table
from reportlab.platypus import Image as ReportLabImage


def csv_para_pdf(arquivo, linhas_por_pagina: int = 40, titulo_pdf: str = "") -> io.BytesIO:
    buffer = io.BytesIO()
    df = pd.read_csv(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    dados = df.values.tolist()
    colunas = df.columns.tolist()
    story = []
    total_linhas = len(dados)
    for i in range(0, total_linhas, linhas_por_pagina):
        story.append(Table([colunas] + dados[i:i + linhas_por_pagina], repeatRows=1))
        if i + linhas_por_pagina < total_linhas:
            story.append(PageBreak())
    doc.build(story)
    buffer.seek(0)
    return buffer


def excel_para_pdf(arquivo, titulo_pdf: str = "") -> io.BytesIO:
    buffer = io.BytesIO()
    df = pd.read_excel(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    doc.build([Table([df.columns.tolist()] + df.values.tolist())])
    buffer.seek(0)
    return buffer


def texto_para_pdf(arquivo, titulo_pdf: str = "") -> io.BytesIO:
    buffer = io.BytesIO()
    texto = arquivo.read().decode("utf-8") if hasattr(arquivo, "read") else open(arquivo, encoding="utf-8").read()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    styles = getSampleStyleSheet()
    doc.build([Paragraph(texto.replace("\n", "<br/>"), styles["Normal"])])
    buffer.seek(0)
    return buffer


def imagem_para_pdf(arquivo, titulo_pdf: str = "") -> io.BytesIO:
    buffer = io.BytesIO()
    img = Image.open(arquivo)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    largura, altura = img.size
    max_largura, max_altura = 400, 600
    if largura > max_largura or altura > max_altura:
        proporcao = min(max_largura / largura, max_altura / altura)
        largura *= proporcao
        altura *= proporcao

    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    doc.build([ReportLabImage(img_buffer, width=largura, height=altura)])
    buffer.seek(0)
    return buffer
