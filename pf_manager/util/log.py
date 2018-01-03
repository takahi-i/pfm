import sys
import logging

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

sh = logging.StreamHandler(sys.stderr)
sh.setLevel(logging.INFO)

logger.addHandler(sh)
