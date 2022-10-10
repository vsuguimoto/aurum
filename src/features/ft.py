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

    df_copy = df_copy.dropna().reset_index(drop=True)

    df_copy.loc[:, 'EMA_BUY_CROSS'] = ta.cross(df_copy.EMA_9, df_copy.EMA_21, asint=False)
    df_copy.loc[:, 'EMA_SELL_CROSS'] = ta.cross(df_copy.EMA_21, df_copy.EMA_9, asint=False)
    df_copy.loc[:, 'EMA_9_DISTANCE'] = df_copy.Close - df_copy.EMA_9 
    df_copy.loc[:, 'EMA_21_DISTANCE'] = df_copy.Close - df_copy.EMA_21

    df_copy.loc[:, 'BBAND_FechouFora_Lower'] = df_copy['Close'] <  df_copy[f'BBL_10_2.0']
    df_copy.loc[:, 'BBAND_FechouFora_Upper'] = df_copy['Close'] >  df_copy[f'BBU_10_2.0']

    return df_copy