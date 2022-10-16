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

def montar_carteira():

    st.markdown('## Monte sua carteira')
    st.markdown('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras porttitor mollis tincidunt.
    Sed fermentum elit lorem, eu finibus nisl maximus nec. Sed eget massa eget ligula blandit tincidunt eu eget lacus.
    ''')
    st.markdown('---')

    st.markdown('**Selecione os ativos para compor sua carteira**')


if __name__=='__main__':
    montar_carteira()