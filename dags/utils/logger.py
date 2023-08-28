"""
Utility script to setup logging universally
"""

import logging
import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s - %(message)s', level=LOG_LEVEL)

log = logging.getLogger(__name__)