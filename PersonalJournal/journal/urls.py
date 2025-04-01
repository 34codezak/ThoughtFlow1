from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    path("", views.home, name="home"),
    path("journal/", views.journal_home, name="journal_home"),
    
    # Profile-related URLs
    path("profile/update/", views.update_profile, name="profile_update"),
    path("profile/", views.profile_detail, name="profile_detail"),

    # Journal Entry CRUD
    path("create/", views.create_entry, name="entry_form"),
    path("update/<int:entry_id>/", views.update_entry, name="update_entry"),
    path("delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("restore/<int:entry_id>/", views.restore_entry, name="restore_entry"),

    # Entries listing
    path("entries/", views.entries_view, name="entries"),
    path("entries/json/", views.get_entries, name="get_entries"),  # JSON API endpoint
]