import streamlit as st
from src.data.data import get_ohlcv
from src.features.ft import technical_indicators, traduzir_nome_colunas
from src.models.model_training import create_setup
from src.utils.utils import display_setup, svg_write

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Análise',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

def main_analysis():

    st.markdown('## Crie seu própio setup')
    st.markdown('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras porttitor mollis tincidunt.
    Sed fermentum elit lorem, eu finibus nisl maximus nec. Sed eget massa eget ligula blandit tincidunt eu eget lacus.
    ''')
    st.markdown('---')

    st.markdown('**Digite o Ticker da ação**')
    
    ANALISE = st.text_input(' ')

    st.markdown('**Selecione os indicadores**')
    INDICADORES = st.multiselect(
        label=' ',
        options=[
        'Distância da Média Móvel Exponencial de 9 períodos',
        'Distância da Média Móvel Exponencial de 21 períodos',
        'Preço fechou fora da Banda de Bollinger Superior',
        'Preço fechou fora da Banda de Bollinger Inferior',
        'Indice de Força Relativa de 14 períodos',
        'Rate of Change de 5 dias',
        'Oscilador Estocástico rápido 14-3-3',
        ],

    )
    
    if st.button('Criar Setup'):

        st.markdown(f'## Setup para {ANALISE}')
        DATA = get_ohlcv(ANALISE)
        DATA = technical_indicators(DATA)
        DATA = traduzir_nome_colunas(DATA)

        TRAIN_SIZE = int(len(DATA) * .75)

        X_train = DATA.loc[TRAIN_SIZE:, INDICADORES]
        y_train = DATA.loc[TRAIN_SIZE:, 'Alvo']

        MODEL = create_setup(X_train, y_train)

        TREE_VIZ = display_setup(MODEL, X_train, y_train)

        SVG = TREE_VIZ.svg()

        svg_write(SVG)


    pass


if __name__=='__main__':
    main_analysis()