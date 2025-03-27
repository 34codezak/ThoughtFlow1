from django.urls import path
from . import views
from journal.views import signup, home, user_logout
from django.contrib.auth.views import LoginView
from .views import signup, user_logout

urlpatterns = [
    path("signup/", views.signup, name="signup"), # Calls the signup function in views.py to handle the signup process
    path("login/", LoginView.as_view(), name="login"), # Uses Django's built-in LoginView but with a custom template
    path("logout/", views.user_logout, name="logout"), # Calls the user_logout function in views.py to handle the logout process and redirect them
    path("", views.home, name="home"), # Calls the home function in views.py to render the home page
    path("profile/update/", views.update_profile, name="update_profile"), # Calls the update_profile function in views.py to render the update profile page
    path("profile/", views.profile_detail, name="profile_detail"),  # Calls the profile_detail function in views.py to render the profile page
    path("create/", views.create_entry, name="create_entry"), # Calls the create_journal_entry function in views.py to render the create journal entry 
    path("update/<int:pk>/", views.update_entry, name="update_entry"), # Calls the update_journal_entry function in views.py to render the update journal entry page
    path("delete/<int:pk>/", views.delete_entry, name="delete_entry"), # Calls the delete_journal_entry function in views.py to render the delete journal entry page
    path("entries/", views.get_entries, name="get_entries"), # Calls the get_entries function in views.py to render the get entries page
    path("profile/update/", views.profile_update, name="profile_update"), # Calls the profile_update function in views.py to render the profile update page
    path(" ", views.journal_home, name="journal_home"), # Calls the home function in views.py to render the journal_home page
    path("entries/", views.entries_view, name="entries"), # Calls the entries_view function in views.py to render the entries page
    path("profile/update/", views.profile_update, name="profile_update"), # Calls the profile_update function in views.py to render the profile update page
    path("profile/", views.profile_detail, name="profile_detail"), # Calls the profile_detail function in views.py to render the profile page
]

