# cd C:\Users\SAMSUNG\repositorio\FTC_analise_de_dados

import folium
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from PIL import Image
from streamlit_folium import folium_static
from haversine import haversine

st.set_page_config( page_title = 'Visão entregador', page_icon = '🛵', layout = 'wide')

#-----------------------
# Funções
#-----------------------

def top_delivers(df1, top_asc):
    df2 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values( ['City', 'Time_taken(min)'], ascending = top_asc ).reset_index()
    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat( [df_aux1, df_aux2, df_aux3]).reset_index( drop = True )
    return df3

def clean_code( df1 ):
    """ Esta funcao tem a responsabilidade de limpar o dataframe
    Tipo de limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de Tempo ( remoção do texto da variável numérica )
    Input: Dataframe
    Output: Dataframe """

    # Removendo dados faltantes
    selecao_linha = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[selecao_linha, :]

    selecao_linha_2 = df['Delivery_person_Ratings'] != 'NaN '
    df1 = df1.loc[selecao_linha_2, :]

    selecao_linha_3 = df1['Time_Orderd'] != 'NaN '
    df1 = df1.loc[selecao_linha_3, :]

    selecao_linha_4 = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[selecao_linha_4, :]

    selecao_linha_5 = df1['Festival'] != 'NaN '
    df1 = df1.loc[selecao_linha_5, :]

    selecao_linha_6 = df1['City'] != 'NaN '
    df1 = df1.loc[selecao_linha_6, :]

    selecao_linha = df1['Weatherconditions'] != 'conditions NaN'
    df1 = df1.loc[selecao_linha, :]

    # Removendo espaço extras
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()


    # Tranformações de dados
    df1['Delivery_person_Age'] = df1.loc[:,'Delivery_person_Age'].astype( int )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1


# ----------------------------------- Início da Estrutura Lógica do Código -----------------------------------
#------------------------------
# Import dataset
#------------------------------
df = pd.read_csv('dataset/train.csv')
#------------------------------
# Limpar código
#------------------------------
df1 = clean_code( df )

# ===========================
# Barra Lateral
# ===========================
st.header('Marketplace - Visão Cliente')

imagem_path = 'logo.png'
image = Image.open(imagem_path)
st.sidebar.image(image, width = 120 )

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider(
            'Até qual valor?',
            value = pd.datetime(2022, 4, 13),
            min_value = pd.datetime(2022, 2, 11),
            max_value = pd.datetime(2022, 4, 6),
            format = 'DD-MM-YYYY')

#st.header( data_slider )
st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect('Quais as condições de trânsito?', ['Low', 'Medium', 'High', 'Jam'], default = ['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Tipo de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]
st.dataframe(df1)

# ========================================
# Layout no Streamlit
# ========================================

tab1, tab2, tab3 = st.tabs(['Visão Geral', '-', '-'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:
            
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de Idade', maior_idade)
            
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Maior de Idade', menor_idade)
            
        with col3:
            melhor_cond = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_cond)
            
        with col4:
            pior_cond = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_cond)
            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('###### Avaliação Médias por Entregador')
            columns = ['Delivery_person_ID', 'Delivery_person_Ratings']
            tab = df1.loc[:, columns].groupby(['Delivery_person_ID']).mean().reset_index()
            st.dataframe( tab )
            
        with col2:
            st.markdown('###### Avaliação Média por Trânsito')
            columns = ['Delivery_person_Ratings' , 'Road_traffic_density']
            x = df1.loc[:, columns].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean', 'std']})
            x.columns = ['delivery_mean', 'delivery_std']
            x = x.reset_index()
            st.dataframe( x )
            
            st.markdown('###### Avaliação Média por Clima')
            columns = ['Delivery_person_Ratings', 'Weatherconditions']
            x = df1.loc[:, columns].groupby(['Weatherconditions']).agg({'Delivery_person_Ratings': ['mean', 'std']})
            x.columns = ['delivery_mean', 'delivery_std']
            x = x.reset_index()
            st.dataframe( x )
        
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2)
        
        with col1:
            top_delivers(df1, top_asc = True)
            st.subheader('Top Entregas Mais Rápidas')
            st.dataframe( df1 )
        
        with col2:
            top_delivers(df1, top_asc = False)
            st.subheader('Top Entregas Mais Lentas')
            st.dataframe( df1 )