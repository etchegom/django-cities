import swapper
from django.db import migrations

from cities.util import add_continents


def create_continents(apps, schema_editor):
    add_continents(swapper.load_model("cities", "Continent"))


def undo_create_continents(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("cities", "0001_initial"),
        swapper.dependency("cities", "Continent"),
    ]

    operations = [
        migrations.RunPython(create_continents, undo_create_continents),
    ]
