from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    """プロジェクトモデル"""
    STATUS_CHOICES = [
        ('planning', '計画中'),
        ('in_progress', '進行中'),
        ('completed', '完了'),
        ('on_hold', '保留中'),
        ('cancelled', 'キャンセル'),
    ]

    name = models.CharField(max_length=200, verbose_name='プロジェクト名')
    description = models.TextField(blank=True, verbose_name='説明')
    client_name = models.CharField(
        max_length=200, blank=True, verbose_name='クライアント名')
    start_date = models.DateField(verbose_name='開始日')
    end_date = models.DateField(verbose_name='終了日')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning',
        verbose_name='ステータス'
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_projects',
        verbose_name='プロジェクトマネージャー'
    )
    members = models.ManyToManyField(
        User,
        related_name='projects',
        blank=True,
        verbose_name='メンバー'
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name='予算'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_overdue(self):
        """期限超過かどうかを判定"""
        if self.status in ['completed', 'cancelled']:
            return False
        return timezone.now().date() > self.end_date

    @property
    def days_remaining(self):
        """残り日数を計算"""
        if self.status in ['completed', 'cancelled']:
            return 0
        delta = self.end_date - timezone.now().date()
        return delta.days if delta.days > 0 else 0
