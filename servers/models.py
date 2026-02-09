from django.db import models

# Create your models here.

class Server(models.Model):
    GAME_CHOICES = (
        ('gta', 'GTA'),
        ('minecraft', 'Minecraft'),
        ('wow', 'WorldOfWarcraft'),
        ('cs', 'Counter'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'inActive')
    )
    name = models.CharField(max_length=64)
    game = models.CharField(max_length=64, choices=GAME_CHOICES)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES)
    cpu_cores = models.PositiveIntegerField()
    RAM = models.PositiveIntegerField()
    traffic = models.PositiveIntegerField()
    price_per_month = models.PositiveIntegerField()