from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Assignment model için admin paneli."""
    list_display = ('item', 'assigned_to', 'assigned_by', 'assigned_at', 'returned_at')
    list_filter = ('assigned_at', 'returned_at')
    search_fields = ('item__name', 'item__serial_number', 'assigned_to__email', 'assigned_by__email')
    raw_id_fields = ('item', 'assigned_to', 'assigned_by')
    date_hierarchy = 'assigned_at'
