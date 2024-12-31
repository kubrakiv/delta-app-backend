# Generated by Django 4.2.6 on 2024-12-22 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0020_orderstatus_orderstatushistory_order_current_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderstatushistory",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="status_history",
                to="base.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderstatushistory",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="status_history",
                to="base.orderstatus",
            ),
        ),
    ]