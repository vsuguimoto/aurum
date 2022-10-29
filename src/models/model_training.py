from src.data.data import get_ohlcv


def full_model_test(TICKER):
    """TODO:
    - Transformar base_indicators em parâmetros;
    - Dar a possibilidade de determinar o parameter grid;
    - Separar as visualizações do treinamento do modelo
        - Levar como parâmetro o modelo salvo

    Args:
        TICKER (_type_): _description_

    Returns:
        _type_: _description_
    """

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pandas_ta as ta
    import seaborn as sns

    from src.data.data import get_ohlcv

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import TimeSeriesSplit

    from dtreeviz.trees import dtreeviz

    df = get_ohlcv(TICKER, DIST_ALVO=5)


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

    df.ta.strategy(base_indicators)
    df['OBV_ROC_14'] = ((df.OBV - df.OBV.rolling(14).mean())/ df.OBV.rolling(14).mean())

    df = df.dropna().reset_index(drop=True)

    df['EMA_BUY_CROSS'] = ta.cross(df.EMA_9, df.EMA_21, asint=False)
    df['EMA_SELL_CROSS'] = ta.cross(df.EMA_21, df.EMA_9, asint=False)
    df['EMA_9_DISTANCE'] = df.Close - df.EMA_9 
    df['EMA_21_DISTANCE'] = df.Close - df.EMA_21

    df['BBAND_FechouFora_Lower'] = df['Close'] <  df[f'BBL_10_2.0']
    df['BBAND_FechouFora_Upper'] = df['Close'] >  df[f'BBU_10_2.0']
    

    FEATURES = [
        'RSI_14', 
        'STOCHd_14_3_3',
        'ROC_2',
        'ROC_5',
        'ROC_10',
        'EMA_BUY_CROSS',
        'EMA_SELL_CROSS',
        'EMA_9_DISTANCE', 
        'EMA_21_DISTANCE',
        'BBAND_FechouFora_Lower', 
        'BBAND_FechouFora_Upper',
        'SLOPE_3',
        'ATRr_5',
        'WILLR_14',
        'OBV_ROC_14'
    ]
    TARGET = ['Alvo']

    train_size = int(len(df) * .85)

    X_train = df.loc[:train_size, FEATURES]
    y_train = df.loc[:train_size, TARGET]

    X_test = df.loc[train_size:, FEATURES]
    y_test = df.loc[train_size:, TARGET]

    param_grid = {
        'random_state': [42],
        'max_depth': [3, 4, 5],
        'min_samples_leaf': [10, 20 , 25, 30, 50],
        'max_features': ['log2', 'sqrt']
    }

    grid_dt = GridSearchCV(
        DecisionTreeClassifier(),
        param_grid = param_grid,
        scoring='accuracy',
        cv=TimeSeriesSplit(4),
        n_jobs=4
    )

    grid_dt.fit(X_train, y_train)

    display(dtreeviz(
        grid_dt.best_estimator_,
        X_train,
        np.ravel(y_train),
        FEATURES,
        TARGET,
        class_names=['Venda', 'Compra']
    ))

    y_pred = [1 if x == True else 0 for x in (grid_dt.best_estimator_.predict_proba(X_test)[:, 1] > .5)]

    resultados = df[train_size:].reset_index(drop=True)
    resultados['PREDICOES'] = y_pred
    resultados['RETORNO_MODELO'] = 1 + ((resultados['LEAK_Retorno']/5)* resultados['PREDICOES'])
    resultados['RETORNO_BNH'] = 1 + ((resultados['LEAK_Retorno']/5))
    resultados['RETORNO_ACUMULADO_MODELO'] = resultados['RETORNO_MODELO'].cumprod()
    resultados['RETORNO_ACUMULADO_BNH'] = 1 + (df['Close'] - df.loc[0, 'Close'])/df.loc[0, 'Close']

    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10,6))
    sns.lineplot(
        y=resultados['RETORNO_ACUMULADO_MODELO'],
        x=resultados['Date'],
        ax=ax[0],
        label='Retorno do Modelo'
    )

    sns.lineplot(
        y=resultados['RETORNO_ACUMULADO_BNH'],
        x=resultados['Date'],
        ax=ax[0],
        label='Retorno Buy and Hold'
    )

    ax[0].set_ylabel('Retorno Acumulado')

    sns.scatterplot(
        y=resultados['PREDICOES'],
        x=resultados['Date'],
        ax=ax[1],
        marker='o',
        linestyle='-'
    )

    ax[1].set_ylabel('Predição')
    ax[1].set_xlabel('Data')
    ax[1].set_yticks([0, 1])
    ax[1].set_yticklabels(['Venda', 'Compra'])

    plt.show()

    return grid_dt.best_estimator_


def train_basic_model(TICKER):

    import joblib

    from src.data.data import get_ohlcv
    from src.features.ft import technical_indicators
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import TimeSeriesSplit

    df = get_ohlcv(TICKER)
    df = technical_indicators(df)

    FEATURES = [
        'RSI_14', 
        'STOCHd_14_3_3',
        'ROC_2',
        'ROC_5',
        'ROC_10',
        'EMA_BUY_CROSS',
        'EMA_SELL_CROSS',
        'EMA_9_DISTANCE', 
        'EMA_21_DISTANCE',
        'BBAND_FechouFora_Lower', 
        'BBAND_FechouFora_Upper',
        'SLOPE_3',
        'ATRr_5',
        'WILLR_14',
        'OBV_ROC_14'
    ]

    TARGET = ['Alvo']

    train_size = int(len(df) * .85)

    X_train = df.loc[:train_size, FEATURES]
    y_train = df.loc[:train_size, TARGET]

    X_test = df.loc[train_size:, FEATURES]
    y_test = df.loc[train_size:, TARGET]

    param_grid = {
        'random_state': [42],
        'max_depth': [4, 5, 6],
        'min_samples_leaf': [10, 20 , 25, 30, 50],
        'max_features': ['log2', 'sqrt']
    }

    grid_dt = GridSearchCV(
        DecisionTreeClassifier(),
        param_grid = param_grid,
        scoring='accuracy',
        cv=TimeSeriesSplit(5),
    )

    grid_dt.fit(X_train, y_train)

    joblib.dump(grid_dt, f'models/Silver - {TICKER}.sav')

    pass


def make_predictions(TICKER):

    import numpy as np
    import joblib

    from src.data.data import get_ohlcv
    from src.features.ft import technical_indicators

    try:
        model = joblib.load(f'models/Silver - {TICKER}.sav')

    except:
        train_basic_model(TICKER)
        model = joblib.load(f'models/Silver - {TICKER}.sav')

    df = get_ohlcv(TICKER, TREINO=False)
    df = technical_indicators(df)

    # TODO: No momento as features estão chumbadas, em tese é necessário ler os metadados
    # do modelo para ser levado em consideração

    FEATURES = [
        'RSI_14', 
        'STOCHd_14_3_3',
        'ROC_2',
        'ROC_5',
        'ROC_10',
        'EMA_BUY_CROSS',
        'EMA_SELL_CROSS',
        'EMA_9_DISTANCE', 
        'EMA_21_DISTANCE',
        'BBAND_FechouFora_Lower', 
        'BBAND_FechouFora_Upper',
        'SLOPE_3',
        'ATRr_5',
        'WILLR_14',
        'OBV_ROC_14'
    ]

    pred = model.predict(df[FEATURES])

    df['RETORNO_MODELO'] = 1 + ((df['LEAK_Retorno']/5) * pred)
    df['RETORNO_ACUMULADO_MODELO'] = df['RETORNO_MODELO'].cumprod()
    df['RETORNO_ACUMULADO_BNH'] = 1 + (df['Close'] - df.loc[0, 'Close'])/df.loc[0, 'Close']

    return df


def create_setup(X_train, y_train):

    from sklearn.tree import DecisionTreeClassifier
    
    dtc = DecisionTreeClassifier(
        random_state = 42,
        max_depth = 4
    )

    dtc.fit(X_train, y_train)

    return dtc


