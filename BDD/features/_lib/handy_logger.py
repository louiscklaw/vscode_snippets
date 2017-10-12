import logging

def setup_logger(sLoggerName):
    """this is a basic console logger facility
        sLoggerName -- logger name
        return -- logger with logger name defined by sLoggerName
    """
    logger = logging.getLogger('handy_behave_run_logger')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger
