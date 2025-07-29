import argparse
import numpy as np
import yfinance as yf
from .data import load_data, preprocess_data
from .model import build_model
from . import logger

def predict_future(ticker, period, window_size, days):
    logger.info(f"Predict para {ticker} período={period}, dias={days}")
    df = yf.download(ticker, period=period)
    prices = df['Close'].values.reshape(-1, 1)
    X, _, scaler = preprocess_data(prices, window_size)
    model = build_model(window_size)
    model.load_weights('model.h5')
    seq = X[-1]
    preds = []
    for _ in range(days):
        pred = model.predict(seq.reshape(1, window_size, 1))[0, 0]
        preds.append(pred)
        seq = np.roll(seq, -1)
        seq[-1] = pred
    preds = scaler.inverse_transform(np.array(preds).reshape(-1, 1))
    for i, p in enumerate(preds, 1):
        print(f"Day {i}: {p[0]:.2f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--period", default="5y")
    parser.add_argument("--window-size", type=int, default=5)
    parser.add_argument("--days", type=int, default=5)
    args = parser.parse_args()
    predict_future(args.ticker, args.period, args.window_size, args.days)

if __name__ == "__main__":
    main()
