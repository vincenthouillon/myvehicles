# Generated by Django 4.1.4 on 2023-01-06 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                ("name", models.CharField(max_length=40, verbose_name="name")),
                ("symbol", models.CharField(max_length=5, verbose_name="symbol")),
                (
                    "symbol_native",
                    models.CharField(max_length=6, verbose_name="symbol native"),
                ),
                ("decimal_digits", models.IntegerField(verbose_name="decimal digit")),
                ("rounding", models.IntegerField(verbose_name="rounding")),
                ("code", models.CharField(max_length=5, verbose_name="code")),
                (
                    "name_plural",
                    models.CharField(max_length=40, verbose_name="name plural"),
                ),
            ],
            options={
                "verbose_name": "devise",
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="AppSettings",
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
                    "distance_unit",
                    models.CharField(
                        choices=[("Km", "kilometers"), ("Mi", "miles")],
                        default="Km",
                        max_length=24,
                        verbose_name="distance unit",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.currency",
                        verbose_name="currency",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "app setting",
            },
        ),
    ]
