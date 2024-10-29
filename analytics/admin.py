from django.contrib import admin

from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'created_at', 'activity_type', 'content_type', 'content_object']
    list_filter = ['activity_type']
    ordering = ['created_at']


admin.site.register(Activity, ActivityAdmin)

