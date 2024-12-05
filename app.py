import pytesseract
import fitz  # PyMuPDF
import re
from collections import defaultdict
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Função para extrair texto do PDF
def extrair_texto_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texto_extraido = ""

    for pagina_num in range(len(doc)):
        pagina = doc.load_page(pagina_num)
        texto_pagina = pagina.get_text("text")
        texto_extraido += texto_pagina
    
    return texto_extraido


def extrair_informacoes_nota(texto):
    informacoes = defaultdict(str)

    cnpj_regex = r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})" 
    cpf_regex = r"(\d{3}\.\d{3}\.\d{3}-\d{2})" 
    empresa_regex =  r"DE\s+(.*?)\s+OS" 
    chave_acesso_regex = r"(\d{4} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4})" 
    data_emissao_regex = r"(\d{2}/\d{2}/\d{4})" 

    cnpjs = re.search(cnpj_regex, texto)
    cpf = re.search(cpf_regex, texto)
    empresa = re.search(empresa_regex, texto)
    chave_acesso = re.search(chave_acesso_regex, texto)
    data_emissao = re.search(data_emissao_regex, texto)

    informacoes["Empresa"] = empresa.group(1)
    informacoes["CNPJs"] = cnpjs.group(1) if cnpjs else ""
    informacoes["CPF"] = cpf.group(1) if cpf else ""
    informacoes["Chave de Acesso"] = chave_acesso.group(1) if chave_acesso else ""
    informacoes["Data de Emissão"] = data_emissao.group(1) if data_emissao else ""

    return informacoes

st.title('Extração de Informações de Nota Fiscal')
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
if uploaded_file is not None:

    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    texto_pdf = extrair_texto_pdf("uploaded_file.pdf")
    informacoes = extrair_informacoes_nota(texto_pdf)

    st.subheader('Informações Extraídas:')

    st.write("Informacoes extraidas da Nota Fiscal:")
    st.write(f"CNPJs: {informacoes['CNPJs']}")
    st.write(f"CPF comprador: {informacoes['CPF']}")
    st.write(f"Empresa: {informacoes['Empresa']}")
    st.write(f"Chave de Acesso: {informacoes['Chave de Acesso']}")
    st.write(f"Data de Emissao: {informacoes['Data de Emissão']}")
