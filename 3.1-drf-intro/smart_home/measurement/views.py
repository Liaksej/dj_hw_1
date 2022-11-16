from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementsSerializer


class SensorsListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementsListView(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer
