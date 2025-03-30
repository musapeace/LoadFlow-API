from django.db import models

class Bus(models.Model):
    voltage = models.FloatField()
    angle = models.FloatField()

class Generator(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    power_output = models.FloatField()

class Load(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    power_demand = models.FloatField()
