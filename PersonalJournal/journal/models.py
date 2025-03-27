from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# User model extension
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics', help_text='Upload Your Profile Picture')
    bio = models.TextField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class JournalEntry(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) # This is a soft delete field

    def __str__(self):
        return self.title
    
# Signal to automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        
# JournalEntry model
class JournalEntry(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) # This is a soft delete field

    def __str__(self):
        return self.title