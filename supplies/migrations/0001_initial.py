# Generated by Django 4.1.4 on 2022-12-20 10:04

from django.db import migrations, models
import django.db.models.deletion
import private_storage.fields
import private_storage.storage.files
import supplies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vehicles", "0002_alter_vehicle_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Supply",
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
                    "vendor",
                    models.CharField(blank=True, max_length=128, verbose_name="vendor"),
                ),
                (
                    "fueltype",
                    models.CharField(
                        choices=[
                            ("diesel", "diesel"),
                            ("petrol", "petrol"),
                            ("ethanol", "ethanol"),
                            ("electric", "electric"),
                            ("cng", "CNG"),
                            ("lpg", "LPG"),
                        ],
                        default="diesel",
                        max_length=24,
                        verbose_name="Fuel type",
                    ),
                ),
                ("date", models.DateField(verbose_name="date")),
                (
                    "mileage",
                    models.IntegerField(blank=True, null=True, verbose_name="mileage"),
                ),
                (
                    "number_of_liters",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=6,
                        null=True,
                        verbose_name="number of liters",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="price"
                    ),
                ),
                (
                    "full_tank",
                    models.BooleanField(default=False, verbose_name="full tank"),
                ),
                (
                    "attachment",
                    private_storage.fields.PrivateFileField(
                        blank=True,
                        null=True,
                        storage=private_storage.storage.files.PrivateFileSystemStorage(),
                        upload_to=supplies.models.upload_doc,
                        verbose_name="file",
                    ),
                ),
                ("note", models.TextField(blank=True)),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fuels",
                        to="vehicles.vehicle",
                    ),
                ),
            ],
            options={
                "verbose_name": "fuel",
                "ordering": ["-date"],
            },
        ),
    ]
