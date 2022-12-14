# cd C:\Users\SAMSUNG\repositorio\FTC_analise_de_dados
#pip install streamlit-folium
# Bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import streamlit as st
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title = 'Visão empresa', page_icon = '📊', layout = 'wide')

#-----------------------
# Funções
#-----------------------
def country_maps( df1 ):
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
                         popup = location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width = 1024, height = 600)

def order_share_by_week( df1 ):
    # Quantidade de pedidos por semana
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    # Número único de entregadores por semana
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    # Para unir 2 df usamos a função "merge"
    df_aux = pd.merge(df_aux1, df_aux2, how = 'inner')
    # Criando uma nova coluna
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.bar(df_aux, x = 'week_of_year', y = 'order_by_deliver')
    return fig

def order_by_week( df1 ):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    df_aux = df1.loc[:, ['ID', 'week_of_year'] ].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return fig

def traffic_order_city( df1 ):
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return fig

def traffic_order_share( df1 ):         
    # Colunas Selecionadas
    columns = ['ID', 'Road_traffic_density']
    # Criação de agrupamento solicitado
    df_aux = df1.loc[:, columns].groupby( 'Road_traffic_density' ).count().reset_index()
    # Criando o Percentual de pedidos por tipo de tráfego
    df_aux['entregas_percent'] = df_aux['ID'] / df_aux['ID'].sum()*100
    fig = px.pie(df_aux, values = 'entregas_percent', names = 'Road_traffic_density')
    return fig

def order_metric( df1 ):
    # selecao de linhas
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
    # Desenhar o gráfico de linhas
    fig = px.bar( df_aux, x = 'Order_Date', y = 'ID' )
    return fig


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

tab1, tab2, tab3 = st.tabs(['Visão Empresa', 'Visão Táticas', 'Visão Geográficas'])

with tab1:
    with st.container():
        # Order Metric
        fig = order_metric( df1 )
        st.markdown('# Ordes by Day')
        st.plotly_chart( fig, use_container_width = True)

    with st.container():
        col1, col2 = st.columns( 2 )
        with col1:
            fig = traffic_order_share( df1 )
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width = True)           

        with col2:
            fig = traffic_order_city( df1 )
            st.header('Traffic Order City')
            st.plotly_chart(fig, use_container_width = True)

with tab2:
    with st.container():
        fig = order_by_week( df1 )
        st.header('Order by Week')
        st.plotly_chart(fig, use_container_width = True)
            
    with st.container():
        fig = order_share_by_week( df1 )
        st.header('Order Share by Week')
        st.plotly_chart(fig, use_container_width = True)

with tab3:
    st.header("Country Maps")
    country_maps( df1 )