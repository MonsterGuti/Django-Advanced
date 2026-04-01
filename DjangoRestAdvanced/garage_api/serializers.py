from rest_framework import serializers
from .models import Manufacturer, Car, Part


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"


class ManufacturerNestedReadSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacturer
        fields = "__all__"


class CarNestedReadSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = "__all__"


class PartManufacturerWriteSerializer(serializers.ModelSerializer):
    # Трябва да дефинираме това поле явно, за да го има в attrs
    manufacturer_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Manufacturer
        fields = (
            'id',
            'manufacturer_id',  # Добавено тук
            'name',
            'country',  # Добавена запетая тук
            'founded_year',
        )
        extra_kwargs = {
            'name': {'required': False},
            'country': {'required': False},
            'founded_year': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        manufacturer_id = attrs.get('manufacturer_id')

        if manufacturer_id is not None:
            try:
                manufacturer_instance = Manufacturer.objects.get(id=manufacturer_id)
                attrs['manufacturer_instance'] = manufacturer_instance
            except Manufacturer.DoesNotExist:
                raise serializers.ValidationError({
                    "manufacturer_id": f"Manufacturer with id {manufacturer_id} does not exist."
                })
            return attrs

        if not attrs.get('name'):
            raise serializers.ValidationError({
                "non_field_errors": "Provide either 'manufacturer_id' or full manufacturer details (name, country, etc.)."
            })

        manufacturer_serializer = ManufacturerSerializer(data=attrs)
        manufacturer_serializer.is_valid(raise_exception=True)

        attrs['manufacturer_data'] = manufacturer_serializer.validated_data

        return attrs


class PartWriteSerializer(serializers.ModelSerializer):
    manufacturer = PartManufacturerWriteSerializer()

    class Meta:
        model = Part
        fields = "__all__"

    @staticmethod
    def resolve_manufacturer(manufacturer_data):
        manufacturer = manufacturer_data.get('manufacturer_instance')

        if manufacturer:
            return manufacturer

        return Manufacturer.objects.create(**manufacturer_data.get('manufacturer_data'))

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        manufacturer = validated_data.pop('manufacturer')

        cars = validated_data.pop('cars', [])

        part = Part.objects.create(
            manufacturer=self.resolve_manufacturer(manufacturer),
            **validated_data
        )

        if cars:
            part.cars.set(cars)

        return part

    def update(self, instance, validated_data):
        manufacturer = validated_data.pop('manufacturer')
        cars = validated_data.pop('cars', [])

        if manufacturer is not None:
            instance.manufacturer = self.resolve_manufacturer(manufacturer)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cars:
            instance.cars.set(cars)

        return instance