# forms.py

from django import forms
from .models import Profile, JournalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["title", "content"]
        
# Form for creating or updating a user's bio and profile picture
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write a short bio about yourself...'}),
        }
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write a short bio about yourself...'}),
        }
        
 
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
        
    
