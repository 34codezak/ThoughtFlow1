from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import JournalEntry
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

# User Signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Login the user in after signing up
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
    user_profile = request.user.profile # Access the oneToOne related profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, "update_profile.html", {"form": form})