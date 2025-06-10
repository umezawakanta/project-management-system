from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Task(models.Model):
    """タスクモデル"""
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '緊急'),
    ]
    
    STATUS_CHOICES = [
        ('todo', '未着手'),
        ('in_progress', '進行中'),
        ('review', 'レビュー中'),
        ('done', '完了'),
        ('cancelled', 'キャンセル'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='プロジェクト'
    )
    title = models.CharField(max_length=200, verbose_name='タイトル')
    description = models.TextField(blank=True, verbose_name='説明')
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='担当者'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='優先度'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo',
        verbose_name='ステータス'
    )
    due_date = models.DateField(null=True, blank=True, verbose_name='期限')
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='見積時間'
    )
    actual_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='実績時間'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
        verbose_name='作成者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = 'タスク'
        verbose_name_plural = 'タスク'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"
    
    @property
    def is_overdue(self):
        """期限超過かどうかを判定"""
        from django.utils import timezone
        if self.status == 'done' or not self.due_date:
            return False
        return timezone.now().date() > self.due_date


class Comment(models.Model):
    """タスクコメントモデル"""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='タスク'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='投稿者'
    )
    content = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    
    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"from django.db import models

# Create your models here.
