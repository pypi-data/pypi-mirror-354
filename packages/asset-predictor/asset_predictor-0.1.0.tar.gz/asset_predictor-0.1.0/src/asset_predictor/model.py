from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from . import logger

def build_model(window_size):
    model = Sequential([
        LSTM(50, input_shape=(window_size, 1)),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, X_train, y_train, epochs=4, batch_size=32):
    logger.info("Iniciando treinamento")
    es = EarlyStopping(monitor='loss', patience=3)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[es])
    model.save('model.h5')
    logger.info("Modelo salvo em model.h5")
    return history
