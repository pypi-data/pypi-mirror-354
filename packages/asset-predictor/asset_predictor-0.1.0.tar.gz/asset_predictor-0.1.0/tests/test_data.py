import numpy as np
import pytest
from src.asset_predictor.data import preprocess_data


def test_preprocess_data():
    prices = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
    window_size = 3

    X, y, scaler = preprocess_data(prices, window_size)

    # Checando formatos esperados das saídas
    assert X.shape == (7, window_size, 1)
    assert y.shape == (7,)

    # Checando valores específicos
    expected_first_X = scaler.transform(np.array([[1], [2], [3]])).reshape(-1, 1)
    expected_first_y = scaler.transform(np.array([[4]]))[0, 0]

    np.testing.assert_array_almost_equal(X[0], expected_first_X)
    assert y[0] == pytest.approx(expected_first_y)

    # Verificando limites de escala
    assert np.min(X) >= 0 and np.max(X) <= 1
    assert np.min(y) >= 0 and np.max(y) <= 1
