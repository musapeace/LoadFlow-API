from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100)
    voltage = models.FloatField()

class Line(models.Model):
    from_bus = models.ForeignKey(Bus, related_name='from_lines', on_delete=models.CASCADE)
    to_bus = models.ForeignKey(Bus, related_name='to_lines', on_delete=models.CASCADE)
    impedance = models.FloatField()

class Load(models.Model):
    bus = models.ForeignKey(Bus, related_name='loads', on_delete=models.CASCADE)
    power = models.FloatField()
