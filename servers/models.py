from decimal import Decimal

from django.db import models

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServerPlan(models.Model):
    title = models.CharField(max_length=64)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    cpu_core = models.PositiveIntegerField()
    RAM = models.PositiveIntegerField()
    storage = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.game} - {self.title}'

class PlanDuration(models.Model):
    plan = models.ForeignKey(ServerPlan, on_delete=models.CASCADE, related_name='plan')
    duration_months = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('plan', 'duration_months')

    def __str__(self):
        return f'{self.plan} - {self.duration_months} months'

    @property
    def discount_percent(self):
        discount = (self.duration_months - 1) * 5
        return min(discount, 30)

    @property
    def total_price(self):
        return self.plan.price * self.duration_months

    @property
    def final_price(self):
        discount = Decimal(self.discount_percent) / Decimal(100)
        total = Decimal(self.total_price)
        return int(total * (Decimal(1) - discount))