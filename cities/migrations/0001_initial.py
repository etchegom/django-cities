import cities.base_models

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import swapper


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AlternativeName",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("name", "Name"),
                            ("abbr", "Abbreviation"),
                            ("link", "Link"),
                            ("iata", "IATA (Airport) Code"),
                            ("icao", "ICAO (Airport) Code"),
                            ("faac", "FAAC (Airport) Code"),
                        ],
                        default="name",
                        max_length=4,
                    ),
                ),
                ("language_code", models.CharField(max_length=100)),
                ("is_preferred", models.BooleanField(default=False)),
                ("is_short", models.BooleanField(default=False)),
                ("is_colloquial", models.BooleanField(default=False)),
                ("is_historic", models.BooleanField(default=False)),
            ],
            options={"swappable": swapper.swappable_setting("cities", "AlternativeName")},
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                (
                    "name_std",
                    models.CharField(db_index=True, max_length=200, verbose_name="standard name"),
                ),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("population", models.IntegerField()),
                ("elevation", models.IntegerField(null=True)),
                ("kind", models.CharField(max_length=10)),
                ("timezone", models.CharField(max_length=40)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="cities",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "cities",
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "City"),
            },
        ),
        migrations.CreateModel(
            name="Continent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                ("code", models.CharField(db_index=True, max_length=2, unique=True)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="continents",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
            ],
            options={
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "Continent"),
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                ("code", models.CharField(db_index=True, max_length=2, unique=True)),
                ("code3", models.CharField(db_index=True, max_length=3, unique=True)),
                ("population", models.IntegerField()),
                ("area", models.IntegerField(null=True)),
                ("currency", models.CharField(max_length=3, null=True)),
                ("currency_name", models.CharField(blank=True, max_length=50, null=True)),
                ("currency_symbol", models.CharField(blank=True, max_length=31, null=True)),
                ("language_codes", models.CharField(max_length=250, null=True)),
                ("phone", models.CharField(max_length=20)),
                ("tld", models.CharField(max_length=5, verbose_name="TLD")),
                ("postal_code_format", models.CharField(max_length=127)),
                ("postal_code_regex", models.CharField(max_length=255)),
                ("capital", models.CharField(max_length=100)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="countries",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
                (
                    "continent",
                    models.ForeignKey(
                        null=True,
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="countries",
                        to=swapper.get_model_name("cities", "Continent"),
                    ),
                ),
                (
                    "neighbours",
                    models.ManyToManyField(
                        related_name="_country_neighbours_+",
                        to=swapper.get_model_name("cities", "Country"),
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "countries",
                "ordering": ["name"],
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "Country"),
            },
        ),
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                (
                    "name_std",
                    models.CharField(db_index=True, max_length=200, verbose_name="standard name"),
                ),
                ("code", models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("population", models.IntegerField()),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="districts",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="districts",
                        to=swapper.get_model_name("cities", "City"),
                    ),
                ),
            ],
            options={
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "District"),
                "unique_together": {("city", "name")},
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                (
                    "name_std",
                    models.CharField(db_index=True, max_length=200, verbose_name="standard name"),
                ),
                ("code", models.CharField(db_index=True, max_length=200)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="regions",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="regions",
                        to=swapper.get_model_name("cities", "Country"),
                    ),
                ),
            ],
            options={
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "Region"),
                "unique_together": {("country", "name")},
            },
        ),
        migrations.CreateModel(
            name="Subregion",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                (
                    "name_std",
                    models.CharField(db_index=True, max_length=200, verbose_name="standard name"),
                ),
                ("code", models.CharField(db_index=True, max_length=200)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="subregions",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="subregions",
                        to=swapper.get_model_name("cities", "Region"),
                    ),
                ),
            ],
            options={
                "abstract": False,
                "swappable": swapper.swappable_setting("cities", "Subregion"),
                "unique_together": {("region", "id", "name")},
            },
        ),
        migrations.CreateModel(
            name="PostalCode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="ascii name"),
                ),
                ("code", models.CharField(max_length=20)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("region_name", models.CharField(db_index=True, max_length=100)),
                ("subregion_name", models.CharField(db_index=True, max_length=100)),
                ("district_name", models.CharField(db_index=True, max_length=100)),
                (
                    "alt_names",
                    models.ManyToManyField(
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "AlternativeName"),
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "City"),
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "Country"),
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "District"),
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "Region"),
                    ),
                ),
                (
                    "subregion",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                        related_name="postal_codes",
                        to=swapper.get_model_name("cities", "Subregion"),
                    ),
                ),
            ],
            options={"swappable": swapper.swappable_setting("cities", "PostalCode")},
        ),
        migrations.AddField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                related_name="cities",
                to=swapper.get_model_name("cities", "Country"),
            ),
        ),
        migrations.AddField(
            model_name="city",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                related_name="cities",
                to=swapper.get_model_name("cities", "Region"),
            ),
        ),
        migrations.AddField(
            model_name="city",
            name="subregion",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=cities.base_models.SET_NULL_OR_CASCADE,
                related_name="cities",
                to=swapper.get_model_name("cities", "Subregion"),
            ),
        ),
        migrations.AlterUniqueTogether(
            name="city", unique_together={("country", "region", "subregion", "id", "name")},
        ),
    ]
