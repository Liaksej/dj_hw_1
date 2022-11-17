from rest_framework import serializers
from django.forms import fields

from measurement.models import Sensor, Measurement


class MeasurementsSerializer(serializers.ModelSerializer):
    photo = fields.ImageField(required=False, allow_empty_file=True)

    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'date_of_measurements', 'photo']


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementsSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
