# create colored logger
import logging

from colorlog import ColoredFormatter


def create_logger(name: str):
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)

  # Create console handler and set level to DEBUG
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)

  # Create formatter
  formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
      "DEBUG": "cyan",
      "INFO": "green",
      "WARNING": "yellow",
      "ERROR": "red",
      "CRITICAL": "red,bg_white",
    },
  )

  # Add formatter to ch
  ch.setFormatter(formatter)

  # Add ch to logger
  logger.addHandler(ch)

  return logger
