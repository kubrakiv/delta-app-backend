# Generated by Django 4.2.6 on 2024-11-20 08:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0017_alter_invoice_currency_rate_alter_invoice_vat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Invoice price",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="total_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Total price",
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="VAT",
            ),
        ),
    ]
