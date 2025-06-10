from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """ユーザープロファイルモデル"""
    ROLE_CHOICES = [
        ('admin', '管理者'),
        ('manager', 'マネージャー'),
        ('developer', '開発者'),
        ('designer', 'デザイナー'),
        ('tester', 'テスター'),
        ('other', 'その他'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='ユーザー'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='電話番号')
    department = models.CharField(
        max_length=100, blank=True, verbose_name='部署')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='other',
        verbose_name='役職'
    )
    bio = models.TextField(blank=True, verbose_name='自己紹介')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='プロフィール画像'
    )
    skills = models.TextField(
        blank=True, verbose_name='スキル', help_text='カンマ区切りで入力')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'ユーザープロファイル'
        verbose_name_plural = 'ユーザープロファイル'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def get_skills_list(self):
        """スキルをリストとして取得"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ユーザー作成時に自動的にプロファイルを作成"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ユーザー保存時にプロファイルも保存"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
