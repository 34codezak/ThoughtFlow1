from django import forms
from .models import Profile

# Form for creating or updating a user's bio and profile picture
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Write a short bio about yourself...'}),
        }