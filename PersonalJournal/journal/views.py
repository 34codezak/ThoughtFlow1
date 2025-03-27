from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import JournalEntry
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Profile
from journal.forms import ProfileUpdateForm

# User Signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request) # Log the user in after signing up
            return redirect("home") # Redirect to the home page
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# Login View
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # Log the user in
            return redirect("home") # Redirect to the home page
    else:
        form = AuthenticationForm()
        
    return render(request, "registration/login.html", {"form": form})

# User logout
def user_logout(request):
    logout(request)
    return redirect("home") # Redirect to the home page

# Home view
def home(request):
    return render(request, "home.html")

# View for updating a user's profile with a LoginRequiredMixin
@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_profile = request.user.profile # Access the oneToOne related profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, "update_profile.html", {"form": form})

@login_required
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "profile/update_profile.html", {"form": form})

@login_required
def profile_update(request):
    user = request.user
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user) # Handling cases where the user does not have a profile
        return redirect("update_profile")
    profile = user.profile
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=user.profile)
    return render(request, "profile/update_profile.html", {"form": form})

def profile_detail(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "profile/profile_detail.html", {"profile": profile})