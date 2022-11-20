def display_setup(MODEL, X_train, y_train):

    from dtreeviz.trees import dtreeviz
    import numpy as np

    VIZ = dtreeviz(
        MODEL,
        X_train,
        np.ravel(y_train),
        feature_names=X_train.columns,
        target_name='Alvo',
        class_names=['Venda', 'Compra'],
        fancy=True,
        scale=1.33,
        histtype='barstacked'
    )

    return VIZ


def svg_write_html(svg, center=True):
    """
    Disable center to left-margin align like other objects.
    """
    import base64
    import streamlit as st

    # Encode as base 64
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")

    # Add some CSS on top
    css_justify = "center" if center else "left"
    css = f'<p style="text-align:center; display: flex; justify-content: {css_justify}">'
    HTML = f'{css}<img src="data:image/svg+xml;base64,{b64}"/>'

    # Write the HTML
    return HTML


def model_results(MODEL_NAME):

    from src.data.data import get_ohlcv
    from src.features.ft import technical_indicators

    import joblib
    import pandas as pd

    TICKER = pd.Series(MODEL_NAME).str.extract('- (.*.).sav')[0][0]

    TEST = get_ohlcv(TICKER, TREINO=False)
    TEST = technical_indicators(TEST)
    
    MODEL = joblib.load(f'models/{MODEL_NAME}')
    TEST['Predicao'] = MODEL.predict(TEST[MODEL.feature_names_in_])

    TEST['Ticker'] = TICKER
    TEST['Retorno do Modelo'] = TEST['Predicao'] * TEST['LEAK_Retorno']/5
    

    RETURN = TEST[['Ticker', 'Date', 'Predicao', 'Retorno do Modelo']]

    return RETURN


def wallet_return(RETURN_LIST, TICKER_WEIGHT):

    import numpy as np
    import pandas as pd

    assert len(RETURN_LIST) == len(TICKER_WEIGHT)
    assert sum(TICKER_WEIGHT) == 1

    
    RETORNO_PONDERADO_MODELO = np.zeros(len(RETURN_LIST[0]))

    for i, retorno in enumerate(RETURN_LIST):

        RETORNO_PONDERADO_MODELO += retorno['Retorno do Modelo'] * TICKER_WEIGHT[i]

    RETORNO_ACUMULADO_MODELO = (1 + RETORNO_PONDERADO_MODELO).cumprod()

    RESULTADOS = pd.DataFrame(RETORNO_ACUMULADO_MODELO)
    RESULTADOS['Date'] = RETURN_LIST[0]['Date']
    RESULTADOS['Retorno da Carteira'] = RETORNO_ACUMULADO_MODELO - 1

    return RESULTADOS[['Date', 'Retorno da Carteira']]


def st_box_modelpredict(TICKER, SINAL):

    """
    Source: https://discuss.streamlit.io/t/style-column-metrics-like-the-documentation/20464/12
    @Shawn_Pereira
    """
    import streamlit as st

    assert SINAL in ('Compra','Sem entrada')
    if SINAL == 'Compra':
        wch_colour_box = (164,199,126)
        wch_colour_font = (33, 33, 33)
        fontsize = 22
        valign = "left"
        iconname = "fas fa-long-arrow-alt-up"
        sline = "Compra"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

    else:
        wch_colour_box = (132, 132, 132)
        wch_colour_font = (33, 33, 33)
        fontsize = 22
        valign = "left"
        iconname = "fas fa-minus"
        sline = "Sem entrada"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'


    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class='{iconname} fa-xs'></i> {TICKER}
                            </style><BR><span style='font-size: 16px; 
                            margin-top: 0;'>{sline}</style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


def st_metric_display(METRIC_VALUE, METRIC_DESCRIPTION):

    """
    Source: https://discuss.streamlit.io/t/style-column-metrics-like-the-documentation/20464/12
    @Shawn_Pereira
    """
    import streamlit as st


    wch_colour_box = (241, 241, 241)
    wch_colour_font = (33, 33, 33)
    fontsize = 24
    valign = "left"



    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 1); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {METRIC_VALUE}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>{METRIC_DESCRIPTION}</style></span></p>"""

    st.markdown(htmlstr, unsafe_allow_html=True)


def st_metric_model_return(RETURN, TICKER):

    import streamlit as st


    if RETURN > 0:
        wch_colour_box = (164,199,126)
        wch_colour_font = (33, 33, 33)
        iconname = "fas fa-plus"

    else:
        wch_colour_box = (199, 127, 125)
        wch_colour_font = (33, 33, 33)
        iconname = "fas fa-minus"
    
    fontsize = 22
    sline = TICKER
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'



    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class='{iconname} fa-xs'></i> {abs(RETURN):.2%}
                            </style><BR><span style='font-size: 16px; 
                            margin-top: 0;'>{sline}</style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


class AuditarModelo:

    import warnings
    warnings.filterwarnings('ignore')
    

    def __init__(self, NOME_MODELO):

        import pandas as pd
        from src.models.model_training import make_predictions

        self.NOME_MODELO = NOME_MODELO
        self.TICKER = pd.Series(NOME_MODELO).str.extract('- (.*.).sav').values[0][0]
        self.MODELO = self.load_model(self.NOME_MODELO)
        self.FEATURES_MODELO = self.MODELO.feature_names_in_
        
        self.TICKER_TEST_DATA = self.load_ticker_test_data(self.TICKER)
        self.MODEL_PREDICTIONS = make_predictions(self.TICKER)

        self.ACCURACY = self.calculate_model_score('ACCURACY')
        self.PRECISION = self.calculate_model_score('PRECISION')
        self.ADPATED_SHARPE_RATIO = self.calculate_adapted_sharpe()
        self.MODEL_CUMULATIVE_RETURN = self.calculate_model_return()
        self.IBOV_BNH_RETURN = self.calculate_ibov_bnh_return()

    def __repr__(self) -> str:
        return f'Auditar Modelo -> {self.NOME_MODELO}'

    def load_model(self, NOME_MODELO):
        import joblib
        
        return joblib.load(f'models/Aurum - {self.TICKER}.sav')

    def load_ticker_test_data(self, TICKER):

        from src.data.data import get_ohlcv
        from src.features.ft import technical_indicators

        df = get_ohlcv(self.TICKER, TREINO=False)
        df = technical_indicators(df)

        return df

    def calculate_model_score(self, score_name):

        import numpy as np
        from sklearn.metrics import accuracy_score, precision_score

        score_map = {'ACCURACY': accuracy_score, 'PRECISION': precision_score}

        y_pred = self.MODELO.predict(self.TICKER_TEST_DATA[self.FEATURES_MODELO])[:-5]
        y_test = np.ravel(self.TICKER_TEST_DATA.dropna(subset='LEAK_Retorno').Alvo)

        metric = score_map[score_name](y_pred=y_pred, y_true=y_test)

        return metric

    
    def calculate_adapted_sharpe(self):

        from src.data.data import get_ohlcv
        from src.models.model_training import make_predictions

        IBOV_DATA = get_ohlcv('BOVA11.SA', TREINO=False)

        IBOV_DATA['RETORNO_DIARIO'] = IBOV_DATA['Close'].pct_change()

        MODEL_RETURN = (self.MODEL_PREDICTIONS.iloc[-26:, :].RETORNO_MODELO.cumprod() - 1).iloc[-6]
        RSK_FREE_RETURN = ((1 + IBOV_DATA.iloc[-26:, :].RETORNO_DIARIO).cumprod() - 1).iloc[-6]
        EXCESS_RETURN = (self.MODEL_PREDICTIONS.RETORNO_MODELO - IBOV_DATA.RETORNO_DIARIO).dropna()

        ADAPTED_SHARPE = (MODEL_RETURN - RSK_FREE_RETURN)/EXCESS_RETURN.std()

        return ADAPTED_SHARPE

    def calculate_model_return(self):

        from src.models.model_training import make_predictions

        MODEL_RETURN = self.MODEL_PREDICTIONS.RETORNO_ACUMULADO_MODELO.dropna().to_list()[-1]

        return MODEL_RETURN

    def calculate_ibov_bnh_return(self):

        from src.data.data import get_ohlcv

        IBOV_DATA = get_ohlcv('BOVA11.SA', TREINO=False)

        IBOV_BNH_RETURN = 1 + (IBOV_DATA.loc[len(IBOV_DATA) - 1, 'Close'] - IBOV_DATA.loc[0, 'Close'])/IBOV_DATA.loc[0, 'Close']

        return IBOV_BNH_RETURN

    def plot_accuracy_over_time(self):

        import plotly.graph_objects as go
        import aurum

        df = self.MODEL_PREDICTIONS[['Date', 'Alvo', 'Predictions']]
        df['TruePositive'] = (df.Alvo == df.Predictions).astype(int)
        df['CumulativeTruePositive'] = df.TruePositive.cumsum()
        df['Acurácia'] = df.CumulativeTruePositive/(df.index + 1)

        # Seleciona-se após 10 dias para normalizar a curva
        df = df.iloc[10:, :]
        
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df.Date,
                y=df.Acurácia,
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

        fig.update_layout(
            plot_bgcolor='#f1f1f1',
            paper_bgcolor='#f1f1f1',
        )


        fig.update_xaxes(
                showgrid=False,
                showticklabels=True,
                fixedrange=True,
                hoverformat='%d/%m/%Y'   
        )

        fig.update_yaxes(
                showgrid=True,
                showticklabels=True,
                tickformat='.0%',
                gridcolor='#CFCFCE',

                fixedrange=True,
                color='#2B2B2B',
                hoverformat='.0%',
                range = [-0.01, 1.01]    
        )

        fig.update_layout(
            title='Acurácia do Modelo ao longo do tempo'
        )
        
        return fig


    def plot_decision_tree(self):

        from dtreeviz.trees import dtreeviz
        import numpy as np

        VIZ = dtreeviz(
            self.MODELO.best_estimator_,
            self.TICKER_TEST_DATA[self.FEATURES_MODELO],
            np.ravel(self.TICKER_TEST_DATA.Alvo),
            feature_names=self.FEATURES_MODELO,
            target_name='Alvo',
            class_names=['Sem sinal', 'Compra'],
            fancy=True,
            scale=1.33,
            histtype='barstacked'
        )

        return VIZ
