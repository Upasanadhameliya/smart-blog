from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Blog
from accounts.models import UserFollow
from interactions.models import BlogInteraction

def home(request):
    if request.user.is_authenticated:
        # Get all users that the current user follows
        followed_users = UserFollow.objects.filter(
            follower=request.user
        ).values_list('following', flat=True)
        
        # Show blogs only from followed users, annotated with interaction counts
        blogs = (
            Blog.objects.filter(author__in=followed_users)
            .select_related('author')
            .annotate(
                view_count=Count('bloginteraction', filter=Q(bloginteraction__interaction_type=BlogInteraction.VIEW)),
                like_count=Count('bloginteraction', filter=Q(bloginteraction__interaction_type=BlogInteraction.LIKE)),
            )
            .order_by('-view_count', '-like_count', '-created_at')
        )

        if not blogs.exists():
            # Empty blogs list if user doesn't follow anyone
            context = {
                'blogs': []
            }
            return render(request, 'blog/home.html', context)
    else:
        # Show all recent blogs for logged-out users, ordered by interactions
        blogs = (
            Blog.objects.all()
            .select_related('author')
            .annotate(
                view_count=Count('bloginteraction', filter=Q(bloginteraction__interaction_type=BlogInteraction.VIEW)),
                like_count=Count('bloginteraction', filter=Q(bloginteraction__interaction_type=BlogInteraction.LIKE)),
            )
            .order_by('-view_count', '-like_count', '-created_at')
        )
    
    context = {'blogs': blogs}
    return render(request, 'blog/home.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    # Record view interaction if user is authenticated
    if request.user.is_authenticated:
        BlogInteraction.objects.get_or_create(
            user=request.user,
            blog=blog,
            interaction_type=BlogInteraction.VIEW
        )
    
    # Get like count and check if current user liked it
    like_count = blog.get_like_count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = BlogInteraction.objects.filter(
            user=request.user,
            blog=blog,
            interaction_type=BlogInteraction.LIKE
        ).exists()
    
    context = {
        'blog': blog,
        'like_count': like_count,
        'user_liked': user_liked
    }
    return render(request, 'blog/blog_detail.html', context)
