import streamlit as st
import pandas as pd
import numpy as np


st.header('Eleições Presidenciais 2022 - Segundo Turno')

DETAILED_URL = ('./resultados2022_1T.csv')
#TOTAL_URL = ('./sim_df.csv')
#POLLS_URL = ('./polls_agreg.csv')

def load_data():
    df = pd.read_csv(DETAILED_URL, sep=";")
    df = df.set_index('Candidato')
 #   total = pd.read_csv(TOTAL_URL)
 #   polls = pd.read_csv(POLLS_URL)
    return df


df = load_data()


st.subheader('Selecione o nível de mobilização do eleitor')

col1, col2, col3 = st.columns(3)
cp =  col1.slider('Eleitores dos candidatos derrotados no 1o.turno que vão dar votos válidos no 2o.turno (%)', 70, 95, 85)
cpbna=  col3.slider('Eleitores que se abstiveram ou votaram branco/nulo no 1o.turno que vão dar votos válidos no 2o.turno (%)', 0, 30, 12)
cp = cp/100
cpbna = cpbna/100

st.subheader('Migração de Votos')
st.write('Escolha a proporção de votos válidos (de 0 a 100%) de cada candidato que irá para Lula. O restante \
será alocado a Bolsonaro. BNA - Brancos, Nulos e Abstenções no 1º turno. A quantidade de votos válidos disponíveis \
para transferência é definida nos parâmetros de mobilizaçáo do eleitor.')

col1, col2, col3 = st.columns(3)
cl = col1.slider('Ciro Gomes -> Lula', 0, 100, 50)
tl = col1.slider('Simone Tebet -> Lula', 0, 100, 50)
sl = col1.slider('Soraya Thronicke-> Lula', 0, 100, 50)
al = col3.slider('Felipe d\'Avila -> Lula', 0, 100, 50)
ol = col3.slider('Outros -> Lula', 0, 100, 50)
bl = col3.slider('BNA -> Lula', 0, 100, 50)
CiroLula = cl/100
TebetLula = tl/100
SorayaLula = sl/100
DavilaLula = al/100
OutrosLula = ol/100
BNALula = bl/100
eleitores = df.sum()
df.loc['Outros'] = df.loc['Padre Kelmon'] + df.loc['Leo Pericles'] +df.loc['Sofia Manzano'] + df.loc['Vera Lucia'] + df.loc['Eymael']  
df.loc['Derrotados'] = df.loc['Ciro'] + df.loc['Tebet'] +df.loc['dAvila'] + df.loc['Soraya'] + df.loc['Outros']  
df.loc['BNA'] = df.loc['Brancos'] + df.loc['Nulos'] +df.loc['Abstencoes']

Lula2T = int(df.loc['Lula'] * 0.98*0.98 ) + int(df.loc['Bolsonaro'] * 0.98*0.01 )+ int(df.loc['Ciro'] * cp * CiroLula )+ int(df.loc['Tebet'] * cp * TebetLula )+ int(df.loc['Soraya'] * cp * SorayaLula )+ int(df.loc['dAvila'] * cp * DavilaLula) + int(df.loc['Outros'] * cp * OutrosLula )+ int(df.loc['BNA'] * cpbna * BNALula )
Bolsonaro2T = int(df.loc['Lula'] * 0.98*0.01 ) + int(df.loc['Bolsonaro'] * 0.98*0.98 )+ int(df.loc['Ciro'] * cp * (1-CiroLula) )+ int(df.loc['Tebet'] * cp * (1-TebetLula) )+ int(df.loc['Soraya'] * cp * (1-SorayaLula) )+ int(df.loc['dAvila'] * cp * (1-DavilaLula)) + int(df.loc['Outros'] * cp * (1-OutrosLula) )+ int(df.loc['BNA'] * cpbna * (1-BNALula) )


container = st.container()
container.subheader('Resultados')
col1, col2, col3 = container.columns(3)
col1.image('./lula.jpg')
col3.image('./bolsonaro.jpg')
col1.metric('Lula',str("{:,.0f}".format(Lula2T)))
col3.metric('Bolsonaro', str("{:,.0f}".format(Bolsonaro2T)))
col1.metric('% votos válidos',str("{:,.2f}".format( round(100*Lula2T/(Lula2T+Bolsonaro2T),2))+"%"))
col3.metric('% votos válidos', str("{:,.2f}".format(round(100*Bolsonaro2T/(Lula2T+Bolsonaro2T),2))+"%"))
st.markdown('#### Resumo')
st.write('Taxa aproximada de comparecimento: '+ str(round(100*((Lula2T+Bolsonaro2T)/0.96/eleitores.values[0]),1))+"%")
st.write('Total de votos válidos: '+ str("{:,.0f}".format(Bolsonaro2T+Lula2T)))
st.write('Votantes do 1ºturno que deram votos válidos no 2ºturno: '+ str("{:,.0f}".format(Bolsonaro2T+Lula2T-int(df.loc['BNA'] * cpbna))))
st.write('Não votantes do 1ºturno que deram votos válidos no 2ºturno: '+ str("{:,.0f}".format(int(df.loc['BNA'] * cpbna)) ))


with st.expander('Notas:'):
    st.write('\
     Este simulador considera que praticamente todos os eleitores que votaram em Lula e Bolsonaro no 1º turno \
     comparecerão no 2º turno (taxa de 98%). A taxa aproximada de comparecimento é calculada \
     supondo que 4\% dos votos no 2º turno foram brancos/nulos')