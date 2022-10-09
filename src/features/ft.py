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

    df_copy['WIKI_SMA_5'] = df_copy['WIKI_daily_views'].rolling(5).mean()
    df_copy['WIKI_SMA_5_Distance'] = df_copy['WIKI_daily_views'] - df_copy['WIKI_SMA_5']
    df_copy['WIKI_Yesterday_diff'] = df_copy['WIKI_daily_views'] - df_copy['WIKI_daily_views'].shift(-1)
    df_copy['WIKI_ROC_5'] = (df_copy['WIKI_daily_views'] / df_copy['WIKI_SMA_5']) * 100

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