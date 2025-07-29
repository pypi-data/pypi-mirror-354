import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Configuração de logs
os.makedirs('logs', exist_ok=True)
logger = logging.getLogger('asset_predictor')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('logs/asset_predictor.log', when='midnight', backupCount=7)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
