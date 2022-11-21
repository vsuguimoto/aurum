import os
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np

from src.utils.utils import model_results, wallet_return, st_box_modelpredict, st_metric_model_return
from src.data.data import get_ohlcv

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Carteira',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

def header():
    st.markdown('## Monte sua carteira')
    st.markdown('''
    Selecione os modelos dos ativos correspondentes para compor sua carteira.
    ''')

    st.subheader('Como funciona a estratégia?')
    st.write('''
    **1º** - Monte sua carteira com até 5 ativos;  
    **2º** - Caso prefira, mude o peso de cada ativo na composição da carteira;  
    **3º** - Verifique se há sinais de Compra no tópico Posições em abertura, caso houver, abra uma posição no ativo de acordo com a proporção estipulada;  
    **4º** - Após 5 dias úteis, finalize a posição.
    ''')
    st.markdown('---')

    st.markdown('**Selecione os ativos para compor sua carteira**')


def montar_carteira():

    header()
    
    MODELOS_SELECIONADOS = st.multiselect(
        'Escolha os ativos',
        options=os.listdir('models'),
        format_func=lambda x: x.split('.')[0],
        max_selections=5 # Limita o número de ativos a serem escolhidos
    )

    if MODELOS_SELECIONADOS != []:
        TICKERS = pd.Series(MODELOS_SELECIONADOS).str.extract('- (.*.).sav')
        VALOR_DEFAULT = 100/len(TICKERS)

        with st.expander('Balancear a carteira',expanded=False):
            PESOS = [atribuir_peso(TICKER,VALOR_DEFAULT) for TICKER in TICKERS[0]]
            
            st.metric(label='Composição percentual final:',value=f'{sum(PESOS)*100:.2f}')

        BOTAO_BALANCEAR_CARTEIRA = st.button('Montar carteira')

        if BOTAO_BALANCEAR_CARTEIRA and sum(PESOS) == 1:

            RESULTADO_MODELOS = [model_results(MODEL) for MODEL in MODELOS_SELECIONADOS]
            RESULTADO_MODELOS_PIVOT = (pd.concat(RESULTADO_MODELOS)
                                         .pivot_table(
                                                index='Date',
                                                columns=['Ticker'],
                                                values=['Predicao', 'Retorno do Modelo'])).tail(10)


            ULTIMA_ABERTURA = RESULTADO_MODELOS_PIVOT.iloc[-1].Predicao.reset_index()
            ULTIMA_ABERTURA['Sinal'] = ['Compra' if x == 1 else 'Sem entrada' for x in ULTIMA_ABERTURA.iloc[:, -1]]

            st.markdown(f'**Posições em abertura para o dia {ULTIMA_ABERTURA.columns[1]:%d/%m/%Y}:**  ')
            COL_POS_ABERTURA = st.columns(5)

            for i, row in ULTIMA_ABERTURA.iterrows():
                with COL_POS_ABERTURA[i]:
                    st_box_modelpredict(TICKER=row.Ticker.replace('.SA',''), SINAL=row.Sinal)


            

            POSICAO_EM_FECHAMENTO = RESULTADO_MODELOS_PIVOT.iloc[-6]
            RESULT_ULT_POSICAO = POSICAO_EM_FECHAMENTO['Retorno do Modelo'][POSICAO_EM_FECHAMENTO.Predicao == 1].reset_index()
            
            st.markdown(f'**Posições em finalização referente ao dia {RESULT_ULT_POSICAO.columns[1]:%d/%m/%Y}:**  ')

            COLS_POS_FINALIZACO = st.columns(5)

            if len(RESULT_ULT_POSICAO) > 0:
                for i, res in RESULT_ULT_POSICAO.iterrows():
                    with COLS_POS_FINALIZACO[i]:
                        st_metric_model_return(TICKER=res.Ticker.replace('.SA',''), RETURN=res.iloc[-1])
            else:
                st.markdown('Sem posições abertas.')



            RESULTS = wallet_return(RESULTADO_MODELOS, PESOS)
  

            st.plotly_chart(plot_retorno_carteira(RESULTS))
        
        elif sum(PESOS) != 1:
            st.warning(f'Ajuste a composição da carteira.')





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


def plot_retorno_carteira(DATA):

    import plotly.graph_objects as go
    import plotly.offline as pyo

    pyo.init_notebook_mode()

    df = DATA.dropna(subset='Retorno da Carteira')

    IBOV_DATA = get_ohlcv('^BVSP', TREINO=False)
    IBOV_DATA = IBOV_DATA[(IBOV_DATA.Date >= df.Date.min()) & (IBOV_DATA.Date <= df.Date.max())].reset_index(drop=True)
    IBOV_DATA['Retorno Buy and Hold'] = (IBOV_DATA['Close'] - IBOV_DATA.loc[0, 'Close'])/IBOV_DATA.loc[0, 'Close']

    figure = go.Figure(
    )


    figure.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Retorno da Carteira'],
            hoverinfo=None,
            name='Retorno da Carteira',
            line={                      
                'color':'#ecab18',
                'shape':'spline',
                'smoothing':0.3,
                'width':3
            }
        )
    )

    figure.add_trace(
        go.Scatter(
            x=IBOV_DATA.Date,
            y=IBOV_DATA['Retorno Buy and Hold'],
            hoverinfo=None,
            name='Retorno do IBOVESPA',
            line={                      
                'color':'#2B2B2B',
                'shape':'spline',
                'smoothing':0.3,
                'width':3
            },
            opacity=.3
        )
    )

    # Atualizando adicionando titulo e mudando cor do Background
    figure.update_layout(
        plot_bgcolor='#f1f1f1',
        paper_bgcolor='#f1f1f1',
        title='Evolução Patrimonial'
    )

    # Atualizando os Eixos
    figure.update_yaxes(
            showgrid=True,
            showticklabels=True,
            tickformat='.0%',
            gridcolor='#CFCFCE',
            fixedrange=True,
            color='#2B2B2B',
            hoverformat='.0%'
            
    )
    figure.update_xaxes(
            showgrid=False,
            showticklabels=True,
            color='#2B2B2B',
            fixedrange=True,
            hoverformat='%d/%m/%Y'
            
    )

    return figure

if __name__== '__main__':
    montar_carteira()