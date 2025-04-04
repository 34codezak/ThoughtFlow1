from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import JournalEntry, Profile
from .forms import ProfileForm, ProfileUpdateForm

# Renamed login function to avoid conflicts
def user_login(request):
    if request.method == "POST":
        print(request.body)
        
        try:
            data = json.loads(request.body)
            title = data.get("title")
            content = data.get("content")
            
            return JsonResponse({"message": "Journal created successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use Django’s login function
            return redirect("home")
    else:
        form = AuthenticationForm()
        
    return render(request, "registration/login.html", {"form": form})

# Fixed signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after signing up
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# User logout
def user_logout(request):
    logout(request)
    return redirect("home")

# Home view
def home(request):
    return render(request, "home.html")

# Fixed profile update
@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("journal:update_profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "profile/update_profile.html")

# Profile detail
@login_required
def profile_detail(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "profile/profile_detail.html", {"profile": profile})

# Fixed `create_entry`
@csrf_exempt
@login_required
def create_entry(request):
    if request.method != "POST":
        try:
            data = json.loads(request.body.decode("utf-8")) # Safely parsing json
            title = data.get("title")
            content = data.get("content")
            
            if not title or not content:
                return JsonResponse({"error": "Title and content are required"}, status=400)
            
            # Save to the database
            entry = JournalEntry.objects.create(title=title, content=content, user=request.user)
            return JsonResponse({"message": "Journal created successfully", "entry_id": entry.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=400)
    """data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")
        entry = JournalEntry.objects.create(title=title, content=content, user=request.user)
        return JsonResponse({"message": "Journal created successfully", "entry_id": entry.id}, status=201)
    """
    # Fix: Return a response for GET requests
    return render(request, "entry_form.html", {"form": None})

# Read entries
@login_required
def view_entries(request):
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False)
    return render(request, "journal/view_entries.html", {"entries": entries})

# Update entry
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
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Delete entry
@csrf_exempt
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "DELETE":
        entry.is_deleted = True
        entry.save()
        return JsonResponse({"message": "Journal moved to trash successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Restore entry
@login_required
def restore_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user, is_deleted=True)
    if request.method == "POST":
        entry.is_deleted = False
        entry.save()
        return JsonResponse({"message": "Journal entry restored successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Get entries
@login_required
def get_entries(request):
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by("-date_posted")
    entries_data = [{"id": e.id, "title": e.title, "content": e.content, "date_posted": e.date_posted} for e in entries]
    return JsonResponse({"entries": entries_data}, status=200)

# Journal home
@login_required
def journal_home(request):
    sort_by = request.GET.get("sort", "-date_posted")
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by(sort_by)
    return render(request, "journal/home.html", {"entries": entries})

# Entries view
@login_required
def entries_view(request):
    sort_by = request.GET.get("sort", "-date_posted")
    entries = JournalEntry.objects.filter(user=request.user, is_deleted=False).order_by(sort_by)
    return render(request, "entries.html", {"entries": entries})
