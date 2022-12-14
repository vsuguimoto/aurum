def wiki_indicators(pagina_wiki, df):
    """_summary_

    Args:
        pagina_wiki (_type_): _description_
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
        
    from src.data.data import get_wiki_pageviews
    
    df_copy = df[:]
    df_copy = get_wiki_pageviews(pagina_wiki, df_copy)

    df_copy.loc[:, 'WIKI_SMA_5'] = df_copy['WIKI_daily_views'].rolling(5).mean()
    df_copy.loc[:, 'WIKI_SMA_5_Distance'] = df_copy['WIKI_daily_views'] - df_copy['WIKI_SMA_5']
    df_copy.loc[:, 'WIKI_Yesterday_diff'] = df_copy['WIKI_daily_views'] - df_copy['WIKI_daily_views'].shift(-1)
    df_copy.loc[:, 'WIKI_ROC_5'] = (df_copy['WIKI_daily_views'] / df_copy['WIKI_SMA_5']) * 100

    return df_copy

def fundamentalist_indicators(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """

    import pandas as pd
    import yfinance as yf

    from src.data.data import get_fund_indicators

    MIN_DATE = df.Date.min() - pd.DateOffset(100)
    MAX_DATE = df.Date.max()


    df_copy = df[:]
    df_copy = df_copy.merge(get_fund_indicators('BRL=X', 'REALDOL', MIN_DATE, MAX_DATE),
                            on=['Date'], how='left')
    df_copy = df_copy.merge(get_fund_indicators('^TNX', 'USTREAS10', MIN_DATE, MAX_DATE),
                            on=['Date'], how='left')
    df_copy = df_copy.merge(get_fund_indicators('CL=F', 'BRENTOIL', MIN_DATE, MAX_DATE),
                            on=['Date'], how='left')


    return df_copy

def technical_indicators(df):
    """_summary_

    Returns:
        _type_: _description_
    """

    import pandas_ta as ta

    df_copy = df[:]

    base_indicators = ta.Strategy(
        name="EDA",
        ta=[
            {'kind': 'rsi'},
            {'kind': 'stoch'},
            {'kind': 'roc', 'length': 2},
            {'kind': 'roc', 'length': 5},
            {'kind': 'roc', 'length': 10},
            {'kind': 'ema', 'length': 9},
            {'kind': 'ema', 'length': 21},
            {'kind': 'bbands', 'length': 10},
            {'kind': 'slope', 'length': 3},
            {'kind': 'atr', 'length': 5},
            {'kind': 'willr'},
            {'kind': 'obv'}

        ]
    )

    df_copy.ta.strategy(base_indicators)
    df_copy.loc[:, 'OBV_ROC_14'] = ((df_copy.OBV - df_copy.OBV.rolling(14).mean())/ df_copy.OBV.rolling(14).mean())

    df_copy = df_copy.dropna(subset=['EMA_21']).reset_index(drop=True)

    df_copy.loc[:, 'EMA_BUY_CROSS'] = ta.cross(df_copy.EMA_9, df_copy.EMA_21, asint=False)
    df_copy.loc[:, 'EMA_SELL_CROSS'] = ta.cross(df_copy.EMA_21, df_copy.EMA_9, asint=False)
    df_copy.loc[:, 'EMA_9_DISTANCE'] = df_copy.Close - df_copy.EMA_9 
    df_copy.loc[:, 'EMA_21_DISTANCE'] = df_copy.Close - df_copy.EMA_21

    df_copy.loc[:, 'BBAND_FechouFora_Lower'] = df_copy['Close'] <  df_copy[f'BBL_10_2.0']
    df_copy.loc[:, 'BBAND_FechouFora_Upper'] = df_copy['Close'] >  df_copy[f'BBU_10_2.0']

    return df_copy

def traduzir_nome_colunas(df):
    """_summary_

    Args:
        df (_type_): _description_
    """

    TRADUTOR = {
        'EMA_9_DISTANCE': 'Dist??ncia da M??dia M??vel Exponencial de 9 per??odos',
        'EMA_21_DISTANCE': 'Dist??ncia da M??dia M??vel Exponencial de 21 per??odos',
        'BBAND_FechouFora_Upper': 'Pre??o fechou fora da Banda de Bollinger Superior',
        'BBAND_FechouFora_Lower': 'Pre??o fechou fora da Banda de Bollinger Inferior',
        'RSI_14': 'Indice de For??a Relativa de 14 per??odos',
        'ROC_5': 'Rate of Change de 5 dias',
        'STOCHk_14_3_3': 'Oscilador Estoc??stico r??pido 14-3-3',
    }

    df_copy = df[:]

    df_copy = df_copy.rename(TRADUTOR, axis=1)

    return df_copy