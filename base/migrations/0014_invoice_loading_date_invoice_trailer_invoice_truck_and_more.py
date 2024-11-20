# Generated by Django 4.2.6 on 2024-11-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0013_alter_invoice_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="loading_date",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="trailer",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="truck",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="invoice",
            name="unloading_date",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
