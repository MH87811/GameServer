from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Game(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


PLAN_LEVEL_CHOICE = (
    (1, 'Bronze'),
    (2, 'Silver'),
    (3, 'Gold'),
    (4, 'Platinum'),
)

class ServerPlan(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='plan')
    cpu_core = models.PositiveIntegerField()
    RAM = models.PositiveIntegerField()
    storage = models.PositiveIntegerField()
    plan_level = models.IntegerField(choices=PLAN_LEVEL_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    has_firewall = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class GameServerPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='game_server')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    plan_level = models.IntegerField(choices=PLAN_LEVEL_CHOICE)
    duration = models.PositiveIntegerField()
    paid_amount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    has_firewall = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)

class DiscountCode(models.Model):
    CODE_TYPE_CHOICES = (
        (1, 'percent'),
        (2, 'value')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discount_code')
    type = models.IntegerField(choices=CODE_TYPE_CHOICES)
    value = models.IntegerField()
    code = models.CharField(max_length=16)
    is_available = models.BooleanField(default=False)
    
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