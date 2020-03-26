import swapper

from .base_models import (
    BaseAlternativeName,
    BaseCity,
    BaseContinent,
    BaseCountry,
    BaseDistrict,
    BasePostalCode,
    BaseRegion,
    BaseSubregion,
)

__all__ = [
    "Continent",
    "Country",
    "Region",
    "Subregion",
    "City",
    "District",
    "PostalCode",
    "AlternativeName",
]


class Continent(BaseContinent):
    class Meta(BaseContinent.Meta):
        swappable = swapper.swappable_setting("cities", "Continent")


class Country(BaseCountry):
    class Meta(BaseCountry.Meta):
        swappable = swapper.swappable_setting("cities", "Country")


class Region(BaseRegion):
    class Meta(BaseRegion.Meta):
        swappable = swapper.swappable_setting("cities", "Region")


class Subregion(BaseSubregion):
    class Meta(BaseSubregion.Meta):
        swappable = swapper.swappable_setting("cities", "Subregion")


class City(BaseCity):
    class Meta(BaseCity.Meta):
        swappable = swapper.swappable_setting("cities", "City")


class District(BaseDistrict):
    class Meta(BaseDistrict.Meta):
        swappable = swapper.swappable_setting("cities", "District")


class AlternativeName(BaseAlternativeName):
    class Meta:
        swappable = swapper.swappable_setting("cities", "AlternativeName")


class PostalCode(BasePostalCode):
    class Meta:
        swappable = swapper.swappable_setting("cities", "PostalCode")
