from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import Profile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Extract cleaned details and create user
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f"Welcome to ShopNova, {username}!")
            return redirect('home')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegisterForm()
            
    return render(request, 'register_test.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please enter valid credentials.")
    else:
        form = UserLoginForm()
            
    return render(request, 'login_test.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        enabled = request.POST.get('notifications_enabled') == 'on'
        profile.notifications_enabled = enabled
        profile.save()
        messages.success(request, f"Notifications are now {'enabled' if enabled else 'disabled'}.")
        return redirect('profile')
        
    return render(request, 'profile_test.html', {'profile': profile})

