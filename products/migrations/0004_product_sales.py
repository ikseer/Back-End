# Generated by Django 4.2.6 on 2023-11-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.PositiveIntegerField(default=0),
        ),
    ]