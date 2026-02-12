from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm
from .models import User, UserFollow

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def authors_list(request):
    """Display list of all authors with follow/unfollow options."""
    # Get all users with 'author' role
    authors = User.objects.filter(role='author').distinct()
    
    # Get list of users the current user is following (if authenticated)
    following_ids = []
    if request.user.is_authenticated:
        following_ids = UserFollow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    
    # Annotate authors with follow status (for template)
    author_data = []
    for author in authors:
        is_following = author.id in following_ids
        author_data.append({
            'author': author,
            'is_following': is_following
        })
    
    context = {
        'authors': author_data,
    }
    return render(request, 'accounts/authors.html', context)


@login_required(login_url='login')
def follow_author(request, pk):
    """Follow an author."""
    author = get_object_or_404(User, pk=pk)
    
    # Prevent users from following themselves
    if author == request.user:
        messages.error(request, "You can't follow yourself!")
        return redirect('authors_list')
    
    # Create or get the follow relationship
    UserFollow.objects.get_or_create(
        follower=request.user,
        following=author
    )
    
    messages.success(request, f'You are now following {author.name or author.username}!')
    return redirect('authors_list')


@login_required(login_url='login')
def unfollow_author(request, pk):
    """Unfollow an author."""
    author = get_object_or_404(User, pk=pk)
    
    # Delete the follow relationship if it exists
    UserFollow.objects.filter(
        follower=request.user,
        following=author
    ).delete()
    
    messages.success(request, f'You are no longer following {author.name or author.username}!')
    return redirect('authors_list')