import logging
import sys
import os

# ========================== #
# ====== Logging init ====== #
# ========================== #

def moduleLogging():
    # Get name of dir
    dirname = os.path.dirname(__file__)

    # Init custom logger
    logger = logging.getLogger(__name__)

    # Init & add handler
    stream_handler = logging.StreamHandler(sys.stdout) # To console
    file_handler = logging.FileHandler(f"{dirname}/../logs/ExtractTable.log", mode='w') # To file
    logger.addHandler(file_handler)

    # Set format of log
    log_format = logging.Formatter(fmt='[%(asctime)s] - %(name)s - {%(levelname)s} - (%(funcName)s, #%(lineno)d) - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)

    # Set min log levels I wanna see
    logger.setLevel(logging.DEBUG)

    # Return logger instance
    return logger