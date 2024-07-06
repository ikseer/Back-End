# -*- coding: utf-8 -*-
from decouple import config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("PORT",default=5432),
        "TEST": {
            "NAME": "my_testdatabase",
        },
       "ATOMIC_REQUESTS": True

    }
}
