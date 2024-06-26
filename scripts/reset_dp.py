# -*- coding: utf-8 -*-
import os
from pathlib import Path

import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()


def reset_migrations(app_name):
    # Navigate to the migrations folder
    migrations_folder = Path(app_name) / "migrations"

    # Delete all migration files except '__init__.py'
    for file in migrations_folder.glob("[0-9]*.py"):
        file.unlink()
    # remove __pycache__
    # rmtree(migrations_folder / "__pycache__")

    # Reset the database
    # call_command('migrate', app_name, 'zero', '--fake')
    # call_command('migrate')


def get_all_apps():
    return [app.split(".")[-1] for app in settings.INSTALLED_APPS]


if __name__ == "__main__":
    # all_apps = get_all_apps()
    all_apps = ["pharmacy", "accounts", "orders", "products"]
    print("Available apps:")

    for app_name in all_apps:
        reset_migrations(app_name)
