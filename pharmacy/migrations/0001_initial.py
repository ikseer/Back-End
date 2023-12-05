# Generated by Django 4.2.6 on 2023-12-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pharmacy_images/')),
                ('open_time', models.TimeField(default='00:00:00')),
                ('close_time', models.TimeField(default='00:00:00')),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
    ]
