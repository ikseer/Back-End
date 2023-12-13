# Generated by Django 4.2.6 on 2023-12-13 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(help_text='Quantity of the product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the medication', max_length=255)),
                ('generic_name', models.CharField(help_text='Generic name of the medication', max_length=255)),
                ('form', models.CharField(help_text='Form of the medication (e.g., tablet, capsule, liquid)', max_length=255)),
                ('strength', models.CharField(help_text='Strength of the medication (e.g., 500mg)', max_length=255)),
                ('factory_company', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('orders', models.ManyToManyField(related_name='products', through='products.OrderItem', to='orders.order')),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.pharmacy')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(help_text='Percentage of discount')),
                ('start_date', models.DateField(blank=True, help_text='Start date of the discount', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End date of the discount', null=True)),
                ('product', models.ForeignKey(help_text='Product for which the discount is applicable', on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
