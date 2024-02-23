from decouple import config

from .base import *

LOCAL = config("LOCAL", cast=bool, default=False)


if LOCAL:
    print("LOCAL MODE")
    from .local import *
else:
    print("PRODUCTION MODE")
    from .production import *
