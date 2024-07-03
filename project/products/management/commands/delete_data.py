import csv
import json

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export data from all models in the database'

    def handle(self, *args, **kwargs):
        from accounts.models import CustomUser

        # Get users where 'delete' is not null
        users_to_delete = CustomUser.objects.exclude(delete__isnull=True)

        # Delete the users
        users_to_delete.delete()
