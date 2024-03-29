import os
import sys
from config import settings

# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(sys.modules['config.settings'], '{0}Config'.format(APP_ENV))()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if '__' not in f]:
   # environment can override anything
   val = os.environ.get(atr, getattr(_current, atr))
   setattr(sys.modules[__name__], atr, val)


# current env
CURRENT_ENV = '{0}Config'.format(APP_ENV)
def as_dict():
   res = {}
   for atr in [f for f in dir(settings) if '__' not in f]:
      val = getattr(settings, atr)
      res[atr] = val
   return res