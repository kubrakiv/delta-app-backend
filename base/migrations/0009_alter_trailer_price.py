# Generated by Django 4.2.6 on 2024-11-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0008_alter_truck_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trailer",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
