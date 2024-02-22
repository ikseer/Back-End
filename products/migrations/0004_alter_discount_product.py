import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_remove_product_orders_delete_orderitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discount",
            name="product",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="products.product"
            ),
        ),
    ]
