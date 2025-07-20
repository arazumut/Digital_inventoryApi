from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Item model için admin paneli."""
    list_display = ('name', 'serial_number', 'category', 'status', 'assigned_to')
    list_filter = ('status', 'category', 'purchase_date')
    search_fields = ('name', 'serial_number', 'notes')
    raw_id_fields = ('assigned_to',)
    date_hierarchy = 'purchase_date'
