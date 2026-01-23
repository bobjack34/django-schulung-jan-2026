from rest_framework import serializers

from events.models import Category, Event


class EventInputSerializer(serializers.ModelSerializer):
    """Ein Serializer für das Anlegen eines Events."""

    class Meta:
        model = Event
        fields = (
            "name",
            "sub_title",
            "description",
            "date",
            "min_group",
            "category",
        )


class EventOutputSerializer(serializers.ModelSerializer):
    """Ein Seralizer für das Anzeigen von Events."""

    class Meta:
        model = Event
        fields = ("id", "name", "date", "min_group", "category")


class CategorySerializer(serializers.ModelSerializer):
    """ein Serializer für das Category - Model."""

    class Meta:
        model = Category
        fields = ("id", "name", "sub_title", "description")


class TemperatureSerializer(serializers.Serializer):
    """
    definiert für eingehende Daten ein Feld: celsius

    data = [
    {"celsius": 3},
    {"celsius": 3},
    ]
    s  = TemperatureSerializer(data=data, many=True)
    """

    celsius = serializers.FloatField()

    def validate_celsius(self, value: float) -> float:
        """wird auf eingehende Daten angewandt."""
        if value < -273.15:
            raise serializers.ValidationError("Wert ist unter dem absoluten Nullpunkt!")
        return value

    def to_representation(self, instance):
        """kann man ausgehende Daten mit weiteren Feldern anreichern."""
        f = instance["celsius"] * 9 / 5 + 32

        return {
            "celsius": instance["celsius"],
            "fahrenheit": round(f, 2),
        }
