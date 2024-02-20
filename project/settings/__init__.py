from decouple import config

LOCAL = config("LOCAL", cast=bool, default=False)

from .base import *

if LOCAL:
    print("LOCAL MODE")
    from .local import *
else:
    print("PRODUCTION MODE")
    from .production import *
