import logging


def get_logger(module_name):
    """
    common logger
    :param module_name:
    :return:
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S %p'
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger