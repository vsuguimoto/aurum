import streamlit as st
import numpy as np
import aurum


TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=TITULO_PROJETO,
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={'About': 'https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config'})

def pagina_principal():
    
    st.title(TITULO_PROJETO)
    
    st.subheader('Utilizando Inteligência Artificial para aumentar seu lucro!')
    st.write('''
    Desenvolvemos diversos modelos de AI com os indicadores técnicos mais utilizados no mercado para simplificar sua tomada de decisão
    poupando seu tempo e melhorando sua assertividade.
    ''')
    
    st.subheader('Faça sua simulação')
    # Nota: o nome do Ticker precisa ser maiúsculo para evitar duplicatas
    # nos modelos treinados - Manter o .upper()
    ANALISE = st.text_input('Digite um ticker de um ativo - Exemplo: PETR4').upper()

    botao = st.button('Analisar')

    if botao:
        # Adiciona o .SA no fim da string ANALISE devido ao formato dos ticker brasileiros
        # no Yahoo Finance
        try:
            try:
                # Necessario manter o .dropna() pelo período de holding da estratégia
                df = aurum.model_training.make_predictions(ANALISE + '.SA').dropna()
            except:
                df = aurum.model_training.make_predictions(ANALISE).dropna()

            h_col1, h_col2 = st.columns(2)
            with h_col1:
                DATA_MIN = df.Date.dt.date.min() 
                st.write(f'''Se tivesse investido **R\$ 1000.00** em **{ANALISE}** no dia {DATA_MIN:%d/%m/%Y},
            hoje seu investimento equivaleria a **R\$ {1000*(df.RETORNO_ACUMULADO_BNH.to_list()[-1]):.2f}**.
            ''')
            with h_col2:
                st.metric('Com nossa estratégia esse valor seria de:', f'R$ {1000*(df.RETORNO_ACUMULADO_MODELO.to_list()[-1]):.2f}')

            st.plotly_chart(plot_returns(df, ANALISE))

            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.metric('Variação percentual:', f'{(df.RETORNO_ACUMULADO_MODELO.to_list()[-1]*100-100):.2f}%')
            with f_col2:
                st.metric('Lucro:', f'R$ {1000*(df.RETORNO_ACUMULADO_MODELO.to_list()[-1])-1000:.2f}')
        except:
            st.error(f'O Ticker **{ANALISE}** não foi encontrado, por favor digite outro.')


    
    st.write('---')
    
    st.subheader('Equipe')
    
    col1, col2, col3 = st.columns(3)
        
    with col1:
        st.markdown('**Jeong Lee**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/jeong-lee-b04937117/)')
        st.markdown('[Github](https://github.com/jeongleeds)')
        
    with col2:
        st.markdown('**Rodrigo Figueiredo**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/rodrigo-figueiredo-73056732)')
        st.markdown('[Github](https://github.com/FIGUEIREDOGITHUB)')

    with col3:
        st.markdown('**Vinicius Suguimoto**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/suguimotovinicius/)')
        st.markdown('[Github](https://github.com/vsuguimoto/)')
    pass


def plot_returns(df, ticker):

    import plotly.graph_objects as go
    import plotly.offline as pyo

    pyo.init_notebook_mode()

    figure = go.Figure(
    )



    figure.add_trace(
        go.Scatter(
            x=df.Date,
            y=df.RETORNO_ACUMULADO_MODELO,
            hoverinfo=None,
            name='Estratégia Aurum',
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
            x=df.Date,
            y=df.RETORNO_ACUMULADO_BNH,
            hoverinfo=None,
            name='Buy and Hold',
            line={                      
                'color':'#2B2B2B',
                'shape':'spline',
                'smoothing':0.3,
                'width':3
            },
            opacity=.5
        )
    )

    # Atualizando adicionando titulo e mudando cor do Background
    figure.update_layout(

        plot_bgcolor='#f1f1f1',
        paper_bgcolor='#f1f1f1',
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
            showticklabels=False,
            fixedrange=True,
            hoverformat='%d/%m/%Y'   
    )

    # Dia com maior preço no último ano
    figure.add_annotation(
            x = df.query('RETORNO_ACUMULADO_MODELO == @df.RETORNO_ACUMULADO_MODELO.max()').Date.to_list()[0],
            y = df.RETORNO_ACUMULADO_MODELO.max(),
            text=f"Maior retorno: {df.RETORNO_ACUMULADO_MODELO.max()*100-100:.2f}%",
            showarrow=False,
            font_size=14,
            yshift=30,
            align='center',
            font_color='#212121',
            bgcolor='#ecab18',
    )

    return figure

if __name__== '__main__':
    pagina_principal()