import logging
from pathlib import Path

def get_logger(name: str, log_file: str = "logs/train.log"):
  logger = logging.getLogger(name)
  if logger.handlers:
    return logger
  logger.setLevel(logging.INFO)
  Path(log_file).parent.mkdir(parents=True, exist_ok=True)
  fh = logging.FileHandler(log_file)
  ch = logging.StreamHandler()
  fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
  fh.setFormatter(fmt); ch.setFormatter(fmt)
  logger.addHandler(fh); logger.addHandler(ch)
  return logger
