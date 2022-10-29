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
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras porttitor mollis tincidunt.
    Sed fermentum elit lorem, eu finibus nisl maximus nec. Sed eget massa eget ligula blandit tincidunt eu eget lacus.
    ''')
    st.markdown('---')

    st.markdown('**Selecione os ativos para compor sua carteira**')


def montar_carteira():

    header()
    
    MODELOS_SELECIONADOS = st.multiselect(
        '',
        options=os.listdir('models'),
        format_func=lambda x: x.split('.')[0],
    # TODO: Adicionar Máximo de inputs
    )

    if MODELOS_SELECIONADOS != []:
        TICKERS = pd.Series(MODELOS_SELECIONADOS).str.extract('- (.*.SA)')

        with st.form('Pesos:'):
            PESOS = [atribuir_peso(TICKER) for TICKER in TICKERS[0]]
            PESOS_SUBMIT = st.form_submit_button("Submit")

        if PESOS_SUBMIT:
            RESULTADO_MODELOS = [model_results(MODEL) for MODEL in MODELOS_SELECIONADOS]
            RESULTS = wallet_return(RESULTADO_MODELOS, PESOS)

            st.plotly_chart(plot_retorno_carteira(RESULTS))





def atribuir_peso(TICKER):

    PESO = st.slider(
        TICKER,
        min_value=0.0,
        max_value=1.0,
        step=.05,
    )

    return PESO


def plot_retorno_carteira(RETORNO):

    import plotly.express as px

    fig = px.line(RETORNO,x='Date', y='Retorno da Carteira')

    return fig



if __name__=='__main__':
    montar_carteira()