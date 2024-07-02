# Generated by Django 4.2.6 on 2024-07-01 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_remove_doctor_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="date_of_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="date_of_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="date_of_birth",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]