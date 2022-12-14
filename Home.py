import streamlit as st
from PIL import Image

st.set_page_config(page_title = "Home", page_icon = "🕹️")

#image_path = "ftc_analise_de_dados/"
image = Image.open('logo.png')
st.sidebar.image( image, width = 120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')

st.markdown(
"""
    Growth Dashboard foi construido para acompanhar as metricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaturantes.
    ### Ask for Help
    - Time de Data Science no Discord
        - oseasoficial1@gmail.com
""")
