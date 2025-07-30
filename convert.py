import io
import pandas as pd
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def csv_para_pdf(arquivo):
    buffer = io.BytesIO()
    df = pd.read_csv(arquivo)
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    dados = [df.columns.tolist()] + df.values.tolist()
    tabela = Table(dados)
    doc.build([tabela])
    return buffer


def excel_para_pdf(arquivo):
    buffer = io.BytesIO()
    df = pd.read_excel(arquivo)
    doc = SimpleDocumentTemplate(buffer, pagesize=letter)
    dados = [df.columns.tolist()] + df.values.tolist()
    tabela = Table(dados)
    doc.build([tabela])
    return buffer


def texto_para_pdf(arquivo):
    buffer = io.BytesIO()
    conteudo = arquivo.read().decode("utf-8")
    doc = SimpleDocumentTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for linha in conteudo.split("\n"):
        if linha.strip():
            p = Paragraph(linha, styles["Normal"])
            story.append(p)

    doc.build(story)
    return buffer


def imagem_para_pdf(arquivo):
    buffer = io.BytesIO()

    # Abre a imagem
    img = Image.open(arquivo)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Cria o PDF
    doc = SimpleDocumentTemplate(buffer, pagesize=letter)
    from reportlab.platypus import Image as ReportLabImage

    largura, altura = img.size

    # Ajusta o tamanho se for muito grande
    max_largura, max_altura = 400, 600
    if largura > max_largura or altura > max_altura:
        proporcao = min(max_largura / largura, max_altura / altura)
        largura *= proporcao
        altura *= proporcao

    # Adiciona a imagem no PDF
    doc.build([ReportLabImage(img_buffer, width=largura, height=altura)])
    return buffer