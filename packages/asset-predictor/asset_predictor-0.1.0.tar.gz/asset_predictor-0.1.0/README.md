# Asset Predictor

Previsão de séries temporais de ativos financeiros usando RNN.

## Instalação

```bash
pip install .
```

## Uso

1. **Download de dados (5 anos)**
   ```bash
   python -m asset_predictor.data --ticker AAPL --period 5y
   ```
2. **Treino (janela 5 dias)**
   ```bash
   python scripts/train.py --ticker AAPL --period 5y --window-size 5 --epochs 10
   ```
3. **Previsão**
   ```bash
   python -m asset_predictor.predict --ticker AAPL --days 5 --window-size 5
   ```

## Logs

Os logs são gravados em `logs/asset_predictor.log` com rotação diária.

## Deploy

```bash
python -m build
twine upload dist/*
```
