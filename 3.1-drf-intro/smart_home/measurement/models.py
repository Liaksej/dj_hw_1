from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='ID датчика')
    temperature = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Температура при измерении')
    date_of_measurements = models.DateField(auto_now=True, verbose_name='Дата измерения')
    photo = models.ImageField(blank=True, null=True, upload_to='photos/')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'
        ordering = ['-date_of_measurements']
