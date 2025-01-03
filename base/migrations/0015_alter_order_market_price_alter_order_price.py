# Generated by Django 4.2.6 on 2024-11-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0014_invoice_loading_date_invoice_trailer_invoice_truck_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="market_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=7,
                null=True,
                verbose_name="Market price",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=7,
                null=True,
                verbose_name="Order price",
            ),
        ),
    ]
