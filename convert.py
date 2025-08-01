import io
import pandas as pd
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet


def csv_para_pdf(arquivo):
    buffer = io.BytesIO()
    df = pd.read_csv(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    dados = [df.columns.tolist()] + df.values.tolist()
    tabela = Table(dados)
    doc.build([tabela])
    buffer.seek(0)
    return buffer


def excel_para_pdf(arquivo):
    buffer = io.BytesIO()
    df = pd.read_excel(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    dados = [df.columns.tolist()] + df.values.tolist()
    tabela = Table(dados)
    doc.build([tabela])
    buffer.seek(0)
    return buffer


def texto_para_pdf(arquivo):
    buffer = io.BytesIO()
    with open(arquivo, "r", encoding="utf-8") as f:
        texto = f.read()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    paragrafo = Paragraph(texto.replace("\n", "<br/>"), styles["Normal"])
    doc.build([paragrafo])
    buffer.seek(0)
    return buffer


def imagem_para_pdf(arquivo):
    buffer = io.BytesIO()
    img = Image.open(arquivo)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    doc = SimpleDocTemplate(buffer, pagesize=letter)
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
