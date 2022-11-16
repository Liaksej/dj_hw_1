from rest_framework import serializers

from measurement.models import Sensor, Measurement


class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'date_of_measurements']


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementsSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
