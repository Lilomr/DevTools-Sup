import pandas as pd
import io
from xhtml2pdf import pisa


def csv_to_pdf(arquivo: io.BytesIO) -> io.BytesIO:
    arq = pd.read_csv(arquivo)
    html_string = arq.to_html(index=False)
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
    return pdf_file
