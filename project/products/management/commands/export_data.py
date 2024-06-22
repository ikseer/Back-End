import csv
import json

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export data from all models in the database'

    def handle(self, *args, **kwargs):
        all_models = apps.get_models()
        all_data = {}

        for model in all_models:
            model_name = model._meta.model_name
            model_data = model.objects.all().values()
            all_data[model_name] = list(model_data)

            # Export JSON
            json_data = json.dumps(list(model_data), indent=4)
            with open(f'data_{model_name}.json', 'w') as json_file:
                json_file.write(json_data)

            # Export CSV
            if model_data:
                with open(f'data_{model_name}.csv', 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(model_data[0].keys())  # Header
                    for obj in model_data:
                        writer.writerow(obj.values())  # Rows

        self.stdout.write(self.style.SUCCESS('All data exported successfully'))
