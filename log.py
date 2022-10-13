import logging
import os

logger = logging.getLogger(__name__)
# log to console
logger.addHandler(logging.StreamHandler())

# check if log folder exists
if not os.path.exists('log'):
    os.mkdir('log')
# log to file
logger.addHandler(logging.FileHandler('log/log.txt'))
if os.environ.get('DEBUG'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

# set log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
for handler in logger.handlers:
    handler.setFormatter(formatter)

