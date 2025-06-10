from django.contrib import admin
from .models import Task, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assignee',
                    'priority', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'project', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    inlines = [CommentInline]

    fieldsets = (
        ('基本情報', {
            'fields': ('project', 'title', 'description')
        }),
        ('担当・優先度', {
            'fields': ('assignee', 'priority', 'status')
        }),
        ('時間管理', {
            'fields': ('due_date', 'estimated_hours', 'actual_hours')
        }),
        ('作成情報', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # 新規作成時
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content']
    date_hierarchy = 'created_at'
