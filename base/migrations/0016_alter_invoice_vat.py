# Generated by Django 4.2.6 on 2024-11-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0015_alter_order_market_price_alter_order_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                max_digits=6,
                null=True,
                verbose_name="VAT",
            ),
        ),
    ]
