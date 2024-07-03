import csv
import json

from django.apps import apps
from django.core.management.base import BaseCommand

from accounts.models.patient import Patient

from safedelete import HARD_DELETE

class Command(BaseCommand):
    help = 'Export data from all models in the database'

    def handle(self, *args, **kwargs):
        from accounts.models import CustomUser

        # Get users where 'delete' is not null
        # users_to_delete = .deleted_objects.all()
        users_to_delete = CustomUser.deleted_objects.all()
        print(len(users_to_delete))
        for user in users_to_delete:
            user.delete(force_policy=HARD_DELETE)
        # Delete the userusers_to_deletes
        # users_to_delete.delete()
