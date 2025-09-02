import io
import pandas as pd
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet


def csv_para_pdf(arquivo, linhas_por_pagina=40, titulo_pdf=""):
    from reportlab.platypus import Table, PageBreak

    buffer = io.BytesIO()
    df = pd.read_csv(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    dados = df.values.tolist()
    colunas = df.columns.tolist()
    story = []
    total_linhas = len(dados)
    for i in range(0, total_linhas, linhas_por_pagina):
        pagina = [colunas] + dados[i : i + linhas_por_pagina]
        tabela = Table(pagina, repeatRows=1)
        story.append(tabela)
        if i + linhas_por_pagina < total_linhas:
            story.append(PageBreak())
    doc.build(story)
    buffer.seek(0)
    return buffer


def excel_para_pdf(arquivo, titulo_pdf=""):
    buffer = io.BytesIO()
    df = pd.read_excel(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    dados = [df.columns.tolist()] + df.values.tolist()
    tabela = Table(dados)
    doc.build([tabela])
    buffer.seek(0)
    return buffer


def texto_para_pdf(arquivo, titulo_pdf=""):
    buffer = io.BytesIO()
    if hasattr(arquivo, "read"):
        texto = arquivo.read().decode("utf-8")
    else:
        with open(arquivo, encoding="utf-8") as f:
            texto = f.read()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    styles = getSampleStyleSheet()
    paragrafo = Paragraph(texto.replace("\n", "<br/>"), styles["Normal"])
    doc.build([paragrafo])
    buffer.seek(0)
    return buffer


def imagem_para_pdf(arquivo, titulo_pdf=""):
    buffer = io.BytesIO()
    img = Image.open(arquivo)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=titulo_pdf)
    from reportlab.platypus import Image as ReportLabImage

    largura, altura = img.size
    max_largura, max_altura = 400, 600
    if largura > max_largura or altura > max_altura:
        proporcao = min(max_largura / largura, max_altura / altura)
        largura *= proporcao
        altura *= proporcao

    doc.build([ReportLabImage(img_buffer, width=largura, height=altura)])
    buffer.seek(0)
    return buffer
