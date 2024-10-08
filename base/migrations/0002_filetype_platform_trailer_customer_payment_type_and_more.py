# Generated by Django 4.2.6 on 2024-08-22 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="Platform",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Trailer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("plates", models.CharField(max_length=25)),
                ("entry_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("vin_code", models.CharField(blank=True, max_length=50, null=True)),
                ("year", models.IntegerField(blank=True, null=True)),
                (
                    "entry_mileage",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("price", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="customer",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="customers",
                to="base.paymenttype",
            ),
        ),
        migrations.AddField(
            model_name="customermanager",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managers",
                to="base.customer",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="market_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                verbose_name="Market price",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="truck",
            name="driver_profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="trucks",
                to="user.driverprofile",
            ),
        ),
        migrations.AddField(
            model_name="truck",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="entry_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="entry_mileage",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="model",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="price",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="vin_code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="truck",
            name="year",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="base.paymenttype",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="base.driver",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="truck",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="base.truck",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="base.tasktype",
            ),
        ),
        migrations.CreateModel(
            name="TrailerAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "trailer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.trailer"
                    ),
                ),
                (
                    "truck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.truck"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(blank=True, null=True, upload_to="order_files/"),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "file_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="file_type",
                        to="base.filetype",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_files",
                        to="base.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DriverAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "driver_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.driverprofile",
                    ),
                ),
                (
                    "truck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.truck"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="platform",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="base.platform",
            ),
        ),
        migrations.AddField(
            model_name="truck",
            name="trailer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="trucks",
                to="base.trailer",
            ),
        ),
    ]
