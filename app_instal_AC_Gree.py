import streamlit as st
from fpdf import FPDF
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
import io
from PIL import Image
import numpy as np
import tempfile 

st.set_page_config('Dados Instalação ar-condicionado Gree', page_icon=':mechanic:')
st.title(':blue[Dados Instalação Ar-Cond GREE]')
st.markdown('<br>', unsafe_allow_html=True)

# Função para gerar PDF
def gera_pdf(dados, assinatura_img):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=14)
    
    # Título do PDF
    pdf.cell(200, 10, txt="Dados para Instalação Ar-Condicionado Gree", ln=True, align='C')
    pdf.ln(10)

    # Dados do Instalador
    pdf.set_font('Arial', style='B', size=12)
    pdf.cell(200, 10, txt="Dados Instalador:", ln=True)
    pdf.set_font('Arial', size=12)
    for key, value in dados['instalador'].items():
        pdf.multi_cell(0, 10, f'{key}: {value}')
    pdf.ln(5)

    # Demais Dados
    pdf.set_font('Arial', style='B', size=12)
    pdf.cell(200, 10, txt="Características da Instalação:", ln=True)
    pdf.set_font('Arial', size=12)
    for key, value in dados['detalhes'].items():
        if value:  # Ignora valores vazios
            pdf.multi_cell(0, 10, f'{key}: {value}')
    pdf.ln(10)

    # Adiciona o título "Assinatura Técnico Responsável"
    pdf.set_font('Arial', style='B', size=12)
    pdf.cell(200, 10, txt="Assinatura Técnico Responsável:", ln=True)
    pdf.set_font('Arial', size=12)
    
    # Se houver uma assinatura, adicionar ao PDF
    if assinatura_img is not None and assinatura_img.size > 0:
        # Converte a imagem de NumPy array para formato que o FPDF aceita
        img = Image.fromarray(assinatura_img)  # Convertendo NumPy array para imagem PIL
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            # Salva a imagem em um arquivo temporário
            img.save(temp_file, format='PNG')
            temp_file_path = temp_file.name

        # Adiciona a imagem ao PDF
        pdf.image(temp_file_path, x=10, y=pdf.get_y(), w=100)  # Adiciona a imagem no PDF

    return pdf.output(dest='S').encode('latin1')

# Dados Empresa Instaladora
st.subheader('Dados Instalador')
dados_instalador = {
    "Instalador": "Marcelo Zagonel Levek",
    "Empresa": "Climátis ar-condicionado e refrigeração Ltda",
    "CNPJ": "52.932.610/0001-27",
    "Endereço": "Rua Itatiaia, 1807 - Portão - Curitiba/Pr",
    "Telefone": "41 9 9613-1762",
}
for key, value in dados_instalador.items():
    st.write(f"**{key}:** {value}")

st.markdown('<br>', unsafe_allow_html=True)

# Sobre o aparelho
st.subheader('Dados Aparelho')
tipo_aparelho = st.selectbox('**Tipo do aparelho:** ', ['Hi Wall', 'Piso Teto', 'Cassete', 'Multisplit'])
modelo = st.text_input('**Modelo:**')

st.markdown('<br>', unsafe_allow_html=True)

# Sobre a instalação
st.subheader('**Características da Instalação**')
dist_teto_evp = st.number_input('Distância do teto Evaporadora: (cm)', min_value=15.0)
espaco_parede_evp = st.number_input('Espaço parede lateral e Evaporadora: (cm)', min_value=15.0)
espaco_teto_cond = st.number_input('Espaço do teto Condensadora: (cm)', min_value=30.0)
dist_parede_cond = st.number_input('Distância parede lateral da Condensadora: (cm)', min_value=30.0)
fixacao_cond = st.radio('Local de fixação da Condensadora?', ['Parede', 'Chão'])
suporte_cond = st.text_input('Tipo de suporte: ') if fixacao_cond == 'Parede' else None
coxim = st.radio('Foi usado coxim de borracha/calços?', ['Sim', 'Não']) if fixacao_cond == 'Chão' else None

tubulacao = st.selectbox('**Tubulação usada:**', ['1/4 e 3/8', '1/4 e 1/2', '1/4 e 5/8', '3/8 e 5/8'])
isolamento = st.radio('**Tipo de Isolamento usado**', ['Polietileno', 'Elastomérico'])
fita_acabamento = st.radio('**Foi Usada Fita de Acabamento?**', ['Sim', 'Não'])
metragem_tub = st.number_input('**Metragem Tubulação**', min_value=3.0)
carga_adicional_gas = st.radio('**Carga Adicional de Fluido?**', ['Não', 'Sim'])
fluido = st.text_input('**Quantidade de gramas de fluido adicional:**') if carga_adicional_gas == 'Sim' else None
vacuo = st.radio('**Realizado Vácuo?**', ['Sim', 'Não'])
microns = st.text_input('Quantos microns: ') if vacuo == 'Sim' else None

st.markdown('<br>', unsafe_allow_html=True)

st.subheader('Outros')
valor_instalacao = st.number_input('**Valor da Instalação:**', min_value=750.00)
data_instalacao = st.text_input('**Data da Instalação (DD/MM/YYYY):**')

st.markdown('<br>', unsafe_allow_html=True)

# Assinatura
st.subheader('Assinatura Técnico Responsável')
canvas_result = st_canvas(
        width=300,
        height=100,
        stroke_width=2,
        stroke_color='black',
        background_color='white',
        display_toolbar=True,
        key='assinatura'
    )


# Botão Salvar PDF
if st.button('Baixar PDF'):
    # Preenche o dicionário com os dados coletados
    dados = {
        "instalador": dados_instalador,
        "detalhes": {
            "Tipo do Aparelho": tipo_aparelho,
            "Modelo": modelo,
            "Distância do Teto Evaporadora (cm)": dist_teto_evp,
            "Espaço da Parede Lateral e Evaporadora (cm)": espaco_parede_evp,
            "Espaço do Teto Condensadora(cm)": espaco_teto_cond,
            "Distância Parede e Condensadora (cm)": dist_parede_cond,
            "Fixação Condensadora": fixacao_cond,
            "Tipo de Suporte": suporte_cond,
            "Usou Coxim": coxim,
            "Tubulação Usada": tubulacao,
            "Isolamento": isolamento,
            "Fita de Acabamento": fita_acabamento,
            "Metragem Tubulação": metragem_tub,
            "Carga Adicional de Fluido": carga_adicional_gas,
            "Quantidade de Fluido": fluido,
            "Vácuo Realizado": vacuo,
            "Microns": microns,
            "Valor da Instalação (R$)": valor_instalacao,
            "Data da Instalação": data_instalacao,
        },
    }

    # Verifica se a assinatura foi desenhada
    if canvas_result.image_data is not None and canvas_result.image_data.size > 0:
        assinatura_img = canvas_result.image_data
        pdf_bytes = gera_pdf(dados, assinatura_img)
        st.download_button(
            label='Download PDF',
            data=pdf_bytes,
            file_name='dados_instal_AC_Gree.pdf',
            mime='application/pdf'
        )
    else:
        st.warning("Por favor, desenhe a assinatura antes de gerar o PDF.")
