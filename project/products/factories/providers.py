import os
import random

import factory
import pandas as pd
from django.conf import settings
from faker.providers import BaseProvider

data_dir = os.path.dirname(os.path.dirname(settings.BASE_DIR))
data_dir=os.path.join(data_dir,'old/data')



class CategoryNameProvider(BaseProvider):
    def category_name(self):
        csv_file=os.path.join(data_dir,'catagory_data.csv')

        categories_df = pd.read_csv(csv_file)

        return random.choice(categories_df['Category_name'])
factory.Faker.add_provider(CategoryNameProvider)
