from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_name', 'status',
                    'manager', 'start_date', 'end_date', 'created_at']
    list_filter = ['status', 'start_date', 'end_date', 'created_at']
    search_fields = ['name', 'client_name', 'description']
    date_hierarchy = 'created_at'
    filter_horizontal = ['members']

    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'description', 'client_name')
        }),
        ('日程', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('担当者', {
            'fields': ('manager', 'members')
        }),
        ('その他', {
            'fields': ('budget',),
            'classes': ('collapse',)
        })
    )
