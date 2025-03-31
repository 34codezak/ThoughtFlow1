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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

# CRUD operations' views
@csrf_exempt
@login_required
# The CREATE logic
def create_entry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        entry = JournalEntry.objects.create(title=title, content=content, user=request.user)
        return JsonResponse({"message": "Journal created successfully", "entry_id": entry.id}, status=201)
    
# The READ logic
def view_entries(request):
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False)
    return render(request, "journal/view_entries.html", {"entries": entries})

# The UPDATE logic
@csrf_exempt
@login_required
def update_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "PUT":
        data = json.loads(request.body)
        entry.title = data.get("title", entry.title)
        entry.content = data.get("content", entry.content)
        entry.save()
        return JsonResponse({"message": "Journal updated successfully"}, status=200)

# The DELETE logic
@csrf_exempt
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "DELETE":
        entry.is_deleted = True
        entry.save()
        return JsonResponse({"message": "Journal moved to trash successfully"}, status=200)
    
@login_required
def restore_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user, is_deleted=True)
    if request.method == "POST":
        entry.restore()
        return JsonResponse({"message": "Journal entry restored successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

    
# The GET logic
@login_required
def get_entries(request):
    entries =  JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by("-created_at")
    entries_data = [{"id": e.id, "title": e.title, "content": e.content, "created_at": e.created_at} for e in entries]
    return JsonResponse({"entries": entries_data}, status=200)

@login_required
def journal_home(request):
    sort_by = request.GET.get("sort", "-created_at") # Default sort by created_at in descending order
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by("-created_at")
    return render(request, "journal/journal_home.html", {"entries": entries})

def entries_view(request):
    # Fetch all journal entries for the logged-in user
    sort_by = request.GET.get("sort", "-created_at") # Default sort by created_at in descending order
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by("-created_at")
    return render(request, "entries.html", {"entries": entries})