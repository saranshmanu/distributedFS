import logging

def configure_logger(file_name):
    logging.basicConfig(filename=file_name,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)

def log_information(func):
    def logger(*args, **kwargs):
        return func(*args, **kwargs)
    return logger