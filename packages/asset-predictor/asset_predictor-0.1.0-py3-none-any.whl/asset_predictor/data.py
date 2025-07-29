import pandas as pd
import numpy as np
from . import logger

def load_data(csv_path):
    logger.info(f"Carregando dados de {csv_path}")
    # df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
    df = pd.read_csv(csv_path, index_col=0)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df[df.index.notna()]  # Corrigido para filtrar diretamente o índice
    prices = df['Close'].values.reshape(-1, 1)
    return prices

def preprocess_data(prices, window_size):
    logger.info(f"Preprocessando dados com window_size={window_size}")
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(prices)
    X, y = [], []
    for i in range(window_size, len(scaled)):
        X.append(scaled[i-window_size:i, 0])
        y.append(scaled[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    return X, y, scaler
