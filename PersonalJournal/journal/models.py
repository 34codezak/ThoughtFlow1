from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) # This is a soft delete field

    def __str__(self):
        return self.title