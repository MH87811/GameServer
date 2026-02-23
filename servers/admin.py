from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ServerPlan)
class ServerPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'cpu_core', 'RAM', 'storage', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(PlanDuration)
class PlanDurationAdmin(admin.ModelAdmin):
    list_display = ('plan', 'duration_months', 'discount_percent', 'total_price', 'final_price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('plan__title',)

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'value', 'code')
    list_filter = ('is_available',)
    search_fields = ('user',)