import os
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np

from src.utils.utils import model_results, wallet_return

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Análise',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

def header():
    st.markdown('## Monte sua carteira')
    st.markdown('''
    Selecione os modelos dos ativos correspondentes para compor sua carteira. Temos dois tipos de modelos
    disponíveis:  
        - Modelos Silver: estratégias desenvolvidas automaticamente pela inteligência artificial com base nos indicadores pré selecionados pelos analistas.  
        - Modelos Gold: estratégias desenvolvidas pelos especialistas utilizando inteligência artificial com indicadores customizados

    **Como funciona:**
    ''')
    st.markdown('---')

    st.markdown('**Selecione os ativos para compor sua carteira**')


def montar_carteira():

    header()
    
    MODELOS_SELECIONADOS = st.multiselect(
        'Escolha os ativos',
        options=os.listdir('models'),
        format_func=lambda x: x.split('.')[0],
    # TODO: Adicionar Máximo de inputs
    )

    if MODELOS_SELECIONADOS != []:
        TICKERS = pd.Series(MODELOS_SELECIONADOS).str.extract('- (.*.).sav')
        VALOR_DEFAULT = 100/len(TICKERS)

        with st.expander('Balancear a carteira',expanded=False):
            #with st.form('Pesos:', clear_on_submit=False):
            PESOS = [atribuir_peso(TICKER,VALOR_DEFAULT) for TICKER in TICKERS[0]]
            st.metric(label='Composição percentual final:',value=sum(PESOS)*100)

        BOTAO_BALANCEAR_CARTEIRA = st.button('Montar carteira')
                #PESOS_SUBMIT = st.form_submit_button("Finalizar")

        if BOTAO_BALANCEAR_CARTEIRA:

            RESULTADO_MODELOS = [model_results(MODEL) for MODEL in MODELOS_SELECIONADOS]
            RESULTS = wallet_return(RESULTADO_MODELOS, PESOS)

            st.plotly_chart(plot_retorno_carteira(RESULTS))





def atribuir_peso(TICKER,VALOR_DEFAULT):

    PESO = st.slider(
        TICKER,
        min_value=0.0,
        max_value=100.0,
        step=5.0,
        value=VALOR_DEFAULT,
        format='%.2f%%'
    )

    return PESO/100


def plot_retorno_carteira(RETORNO):

    import plotly.express as px

    fig = px.line(RETORNO,x='Date', y='Retorno da Carteira')

    return fig



if __name__=='__main__':
    montar_carteira()