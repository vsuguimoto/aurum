import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Análise',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

def main_analysis():

    st.markdown('## Sobre')
    st.markdown('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras porttitor mollis tincidunt.
    Sed fermentum elit lorem, eu finibus nisl maximus nec. Sed eget massa eget ligula blandit tincidunt eu eget lacus.
    ''')
    st.markdown('---')

    st.markdown('**Selecione uma ação para ser analisada**')
    
    ANALISE = st.text_input(' ')
    
    if ANALISE != '':
        st.plotly_chart(grafico_preco(ANALISE))
        st.plotly_chart(histograma_preco(ANALISE))
        
    pass



def dados_acoes(ticker):
    
    ticker = yf.Ticker(ticker)
    
    data_d = ticker.history(
    period='5y',
    interval='1d'
    ).reset_index()
    
    # Cálculo do Retorno
    data_d['Return'] = ((data_d['Close'] - data_d['Open'] + data_d['Dividends'])/data_d['Open']) * 100
    
    return data_d

def grafico_preco(ticker):
    
    dados = dados_acoes(ticker)
    
    fig = px.line(
        data_frame=dados,
        x='Date',
        y='Close',
        title=f'Preço de Fechamento da {ticker}'
    )
    
    return fig

def histograma_preco(ticker):
    
    dados = dados_acoes(ticker)
    
    fig = px.histogram(
        data_frame=dados,
        x='Return',
        title=f'Retorno da {ticker}',
    )
    return fig

if __name__=='__main__':
    main_analysis()