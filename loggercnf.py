import logging
import os

# Forming path
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'mainapp')
# Base logger settings.
logging.basicConfig(
    filename='mainapp.log',
    format='%(asctime)s %(levelname)s %(filename)s %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO
)
# register
logger = logging.getLogger('mainapp.log')
