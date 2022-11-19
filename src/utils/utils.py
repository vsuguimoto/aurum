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
        fancy=False,
        scale=1.33,
        histtype='barstacked'
    )

    return VIZ


def svg_write(svg, center=True):
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
    html = f'{css}<img src="data:image/svg+xml;base64,{b64}"/>'

    # Write the HTML
    st.write(html, unsafe_allow_html=True)


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
    RESULTADOS['Retorno da Carteira'] = RETORNO_ACUMULADO_MODELO

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