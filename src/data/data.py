'''
Criado por: Vinicius Suguimoto
'''

def get_ohlcv(TICKER, SUAVIZAR=False, DIST_ALVO=5, ENTRADA_SAIDA_MODELO='Close'):
    """### Descrição:
    Baixa os dados do ticker do Yahoo Finance e computa automaticamente o alvo de acordo com a distância presente no
    parâmetro DIST_ALVO. O alvo é binário, considerado como subiu ou caiu, será 1 quando o retorno for maior que 0.

    ### Notas:
    - !!CASO UTILIZAR A ENTRADA COMO "Open" TERÁ VAZAMENTO DE DADOS!!;
    - O retorno não leva em conta a distribuição de dividendos;
    - O retorno não leva em conta o split de ações.

    ### Args:
        TICKER (str): Ticker do Yahoo Finance.
        SUAVIZAR (bool, optional): Suaviza os dados OHLC com uma média móvel com alpha de 0,5. Defaults to False.
        DIST_ALVO (int, optional): Número de dias no futuro para o retorno ser calculado, ou seja, o tempo que se permanece
        na operação. Defaults to 1.
        ENTRADA_SAIDA_MODELO (str, optional): "Open" ou "Close", é a entrada do modelo. Defaults to 'Close'.

    ### Returns:
        pandas.Dataframe: Retorna um dataframe com dados OHLC, retorno e alvo.
    """

    import pandas as pd
    import yfinance as yf

    ticker = yf.Ticker(TICKER) 

    df = ticker.history(
        start='2017-01-01',
        end='2022-06-01',
        interval='1d',
    ).reset_index()

    assert DIST_ALVO > 0, 'O número de dias paro o alvo precisa ser maior ou igual a zero.'
    assert ENTRADA_SAIDA_MODELO in ['Open', 'Close'], 'A entrada e saída do modelo precisa ser igual a "Open" ou "Close".'

    df['LEAK_Retorno'] = (df[ENTRADA_SAIDA_MODELO].shift(-DIST_ALVO) - df[ENTRADA_SAIDA_MODELO])/df[ENTRADA_SAIDA_MODELO].shift(-DIST_ALVO)
    df['Alvo'] = (df['LEAK_Retorno'] > 0.00).astype('int')


    if SUAVIZAR == True:
        ALPHA_FACTOR = .5
        df['Open'] = df.Open.ewm(alpha=ALPHA_FACTOR).mean()
        df['Close'] = df.Close.ewm(alpha=ALPHA_FACTOR).mean()
        df['High'] = df.High.ewm(alpha=ALPHA_FACTOR).mean()
        df['Low'] = df.Low.ewm(alpha=ALPHA_FACTOR).mean()

    return df

def get_wiki_pageviews(PAGE, df):
    """Fonte: https://wikimedia.org/api/rest_v1/

    Args:
        PAGE (str): Final da URL da página da Wikipedia.
        df (pandas.DataFrame): Dataframe a ser enriquecido com dados de visualização do Wikipedia.

    Returns:
        pandas.DataFrame: Dataframe enriquecido com dados da Wikipedia
    """

    import random
    import requests
    import json
    import pandas as pd
    
    # Período analisado
    DATEMIN = df.Date.dt.strftime('%Y%m%d').min()
    DATEMAX = df.Date.dt.strftime('%Y%m%d').max()

    # Endpoint da API
    URL = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/pt.wikipedia.org/all-access/all-agents/{PAGE}/daily/{DATEMIN}/{DATEMAX}'

    USER_AGENTS = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    ]   

    response = requests.get(
        URL,
        headers={"user-agent" : random.choice(USER_AGENTS)}
    )

    content_json = json.loads(response.content)
    results_df = pd.DataFrame.from_dict(content_json['items'])[['timestamp', 'views']]
    results_df['timestamp'] = pd.to_datetime([x[:-2] for x in results_df.timestamp])

    results_df = results_df.rename({'views': 'WIKI_daily_views', 'timestamp': 'Date'}, axis=1)

    final_df = df[:]
    final_df = final_df.merge(right=results_df, on='Date')

    return final_df

def gerar_dataset(TICKER):
    """TODO: Criar Dataset padrão para inputar features

    Args:
        TICKER (_type_): _description_

    Returns:
        _type_: _description_
    """
    return None