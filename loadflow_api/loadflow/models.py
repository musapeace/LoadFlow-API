from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    voltage = models.FloatField(default=1.0)
    type = models.CharField(
        max_length=10,
        choices=[('SLACK', 'Slack'), ('PV', 'PV'), ('PQ', 'PQ')],
        default='PQ'
    )

class Line(models.Model):
    from_bus = models.ForeignKey(Bus, related_name='from_lines', on_delete=models.CASCADE)
    to_bus = models.ForeignKey(Bus, related_name='to_lines', on_delete=models.CASCADE)
    impedance_real  = models.FloatField()
    impedance_imag = models.FloatField()

class Load(models.Model):
    bus = models.ForeignKey(Bus, related_name='loads', on_delete=models.CASCADE)
    load_real = models.FloatField()
    load_imag = models.FloatField()

