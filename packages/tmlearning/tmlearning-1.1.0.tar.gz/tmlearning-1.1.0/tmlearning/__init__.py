# IMPORTS

import ctypes

from .tmlearner import TMLearner
from .key_test import wasd_key_test, arrow_key_test

# ASSERT ADMIN
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    raise Exception("keyboard module must have administrator privileges to work correctly. Re-run with administrator privileges.")