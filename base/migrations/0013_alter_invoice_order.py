# Generated by Django 4.2.6 on 2024-11-17 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0012_rename_account_number_companybank_account_number_cz_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invoice",
                to="base.order",
            ),
        ),
    ]
