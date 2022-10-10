import streamlit as st
import numpy as np

TITULO_PROJETO = 'Aurum'

st.set_page_config(
        page_title=TITULO_PROJETO,
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={'About': 'https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config'})

def pagina_principal():
    
    st.title(TITULO_PROJETO)
    
    st.subheader('Utilizando Inteligência Artificial para te aumentar seu lucro!')
    st.write('''
    Treinamos diversos modelos de AI com os indicadores técnicos mais utilizados no mercado para simplificar sua tomada de decisão
    poupando seu tempo e melhorando sua assertividade.
    ''')
    
    st.subheader('Faça sua simulação')
    ANALISE = st.text_input(' ')

    botao = st.button('Analisar')

    if botao:
        df = make_predictions(ANALISE)

        h_col1, h_col2 = st.columns(2)
        with h_col1:
            st.write(f'''Se tivesse investido **R\$ 1000.00** em **{ANALISE}** há um ano,
        hoje seu investimento equivaleria a **R\$ {1000*(df.BnH_Cum_Return.to_list()[-1]):.2f}**.
        ''')
        with h_col2:
            st.metric('Com nossa estratégia esse valor seria de:', f'R$ {1000*(df.Pred_Cum_Return.to_list()[-2]):.2f}')

        st.plotly_chart(plot_returns(df, ANALISE))

        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.metric('Variação percentual:', f'{(df.Pred_Cum_Return.to_list()[-2]*100):.2f}%')
        with f_col2:
            st.metric('Lucro:', f'R$ {1000*(df.Pred_Cum_Return.to_list()[-2])-1000:.2f}')


    st.write('---')
    
    st.subheader('Equipe')
    
    r1col1, r1col2 = st.columns(2)
        
    with r1col2:
        st.markdown('**Jeong Lee**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/jeong-lee-b04937117/)')
        st.markdown('[Github](https://github.com/jeongleeds)')
        
    
    r2col1, r2col2 = st.columns(2)
    with r2col1:
        st.markdown('**Rodrigo Figueiredo**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/rodrigo-figueiredo-73056732)')

    with r2col2:
        
        st.markdown('**Vinicius Suguimoto**')
        st.markdown('[Linkedin](https://www.linkedin.com/in/suguimotovinicius/)')
        st.markdown('[Github](https://github.com/vsuguimoto/)')
    pass


# Funções Auxiliares
def dados_acoes(ticker):
    """Consome a API do Yahoo Finance para retornar a série histórica dos últimos 5 anos de um papel no intervalo diário.

    Args:
        ticker ('string'): Ticker do papel no Yahoo Finance

    Returns:
        pandas.DataFrame: Dataframe contendo os preços OHLC e o retorno do ativo
    """
    
    import yfinance as yf

    ticker = yf.Ticker(ticker)
    
    data_d = ticker.history(
        period='5y',
        interval='1d'
    ).reset_index()
    
    # Cálculo do Retorno
    data_d['Return'] = ((data_d['Close'] - data_d['Open'] + data_d['Dividends'])/data_d['Open'])

    # Cálculo do Target padrão
    # TODO: Criar função específica para isso
    ALVO_PERCENT = 0.5/100
    data_d['TomorrowReturn'] = data_d['Return'].shift(-1) 
    data_d['Target'] = [1 if x >= ALVO_PERCENT else 0 for x in data_d['TomorrowReturn']]

    
    return data_d


def dados_acoes_1y(ticker):
    """Consome a API do Yahoo Finance para retornar a série histórica dos último ano de um papel no intervalo diário.

    Args:
        ticker ('string'): Ticker do papel no Yahoo Finance

    Returns:
        pandas.DataFrame: Dataframe contendo os preços OHLC e o retorno do ativo
    """
    
    import yfinance as yf

    ticker = yf.Ticker(ticker)
    
    data_d = ticker.history(
        period='1y',
        interval='1d'
    ).reset_index()
    
    # Cálculo do Retorno
    data_d['Return'] = ((data_d['Close'] - data_d['Open'] + data_d['Dividends'])/data_d['Open'])
    
    # Cálculo do Target padrão
    # TODO: Criar função específica para isso
    ALVO_PERCENT = 0.5/100
    data_d['TomorrowReturn'] = data_d['Return'].shift(-1) 
    data_d['Target'] = [1 if x >= ALVO_PERCENT else 0 for x in data_d['TomorrowReturn']]

    return data_d


def train_baseline_model(ticker):
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    import joblib
    

    df = dados_acoes(ticker)
    df['TomorrowReturn'] = df['Return'].shift(-1)

    # Separação em treino e test
    train_proportion = .70
    size_train = int(len(df)*train_proportion)

    train = df[:size_train]
    test  = df[size_train:]


    ## Seleção de Features e Targets
    FEATURES = ['Return']
    TARGET = ['Target']

    x_train = train[FEATURES]
    y_train = train[TARGET]


    default_pipe = Pipeline(
        [
        ('Scaling', StandardScaler()),
        ]
    )
    
    x_train_transformed = default_pipe.fit_transform(x_train)

    dtc = DecisionTreeClassifier(random_state=42, class_weight='balanced')

    dtc.fit(x_train_transformed, y_train)

    joblib.dump(default_pipe, f'models/pipe_{ticker}.sav')
    joblib.dump(dtc, f'models/model_{ticker}.sav')

    pass


def make_predictions(ticker):

    import numpy as np
    import joblib

    try:
        pipe = joblib.load(f'models/pipe_{ticker}.sav')
        model = joblib.load(f'models/model_{ticker}.sav')

    except:
        train_baseline_model(ticker)

        pipe = joblib.load(f'models/pipe_{ticker}.sav')
        model = joblib.load(f'models/model_{ticker}.sav')
        
    df = dados_acoes_1y(ticker)

    x_test = df[['Return']]
    x_test_transformed = pipe.transform(x_test)


    pred = model.predict(x_test_transformed)

    df['Predictions'] = pred

    ## Lógica:
    # Se minha previsão foi positiva, entrei na operação
    # Note que operamos apenas na ponta compradora
    # Codigo redundante por não operarmos na ponta vendedora
    df['Pred_Mask'] = np.where(
        (df.Predictions == 1), 1, 0
    )

    df['Pred_Return'] =  df['Pred_Mask'] * df['TomorrowReturn']
    df['Pred_Cum_Return'] = (1 + df.Pred_Return).cumprod()

    # Buy and Hold Return 
    df['BnH_Cum_Return'] = 1 + ((((df['Close'] - df['Open'][0]) + df['Dividends'])/df['Open'][0]))

    return df


def plot_returns(df, ticker):

    import plotly.graph_objects as go
    import plotly.offline as pyo

    pyo.init_notebook_mode()

    figure = go.Figure(
    )



    figure.add_trace(
        go.Scatter(
            x=df.Date,
            y=df.Pred_Cum_Return,
            hoverinfo=None,
            name='Estratégia Aurum',
            line={                      
                'color':'#FF7E66',
                'shape':'spline',
                'smoothing':0.3,
                'width':3
            }
        )
    )

    figure.add_trace(
        go.Scatter(
            x=df.Date,
            y=df.BnH_Cum_Return,
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

        plot_bgcolor='#F7F7F7',
        paper_bgcolor='#F7F7F7',
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
            x = df.query('Pred_Cum_Return == @df.Pred_Cum_Return.max()').Date.to_list()[0],
            y = df.Pred_Cum_Return.max(),
            text=f"Maior retorno: {df.Pred_Cum_Return.max()*100-100:.2f}%",
            showarrow=False,
            font_size=14,
            yshift=30,
            align='center',
            font_color='#050505',
            bgcolor='#FF7E66',
    )

    return figure

if __name__== '__main__':
    pagina_principal()