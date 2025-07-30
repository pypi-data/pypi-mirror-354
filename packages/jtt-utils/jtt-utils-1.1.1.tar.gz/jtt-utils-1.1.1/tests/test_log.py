import logging
logger = logging.getLogger('a')
logger2 = logging.getLogger('a')
print(logger==logger2)
print(__name__)