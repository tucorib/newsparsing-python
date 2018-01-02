import logging

# Define console logger
logger = logging.getLogger("pyhocon.config_parser")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
