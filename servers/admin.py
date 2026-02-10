from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ServerPlan)
class ServerPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'cpu_core', 'RAM', 'storage', 'price', 'is_active', 'created_at')
    list_filter = ('game', 'is_active')
    search_fields = ('title', 'game__name')


@admin.register(PlanDuration)
class PlanDurationAdmin(admin.ModelAdmin):
    list_display = ('plan', 'duration_months', 'discount_percent', 'total_price', 'final_price', 'is_active')
    list_filter = ('plan__game', 'is_active')
    search_fields = ('plan__title', 'plan__game__name')