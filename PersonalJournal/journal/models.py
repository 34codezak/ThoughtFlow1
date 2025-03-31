from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# User model extension
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        help_text='Upload Your Profile Picture'
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class JournalEntry(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journal_entries'
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Added missing field
    
    def soft_delete(self):
        """Marks the entry as deleted without actually removing it."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        
    def restore(self):
        """Restores a soft-deleted entry."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Journal Entry')
        verbose_name_plural = _('Journal Entries')
        ordering = ['-date_posted']


# Signal to automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()