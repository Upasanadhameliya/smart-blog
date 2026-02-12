from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blog.models import Blog
from .models import BlogInteraction

@login_required(login_url='login')
def like_blog(request, pk):
    """Toggle like on a blog post."""
    blog = get_object_or_404(Blog, pk=pk)
    
    # Try to get existing like interaction
    interaction, created = BlogInteraction.objects.get_or_create(
        user=request.user,
        blog=blog,
        interaction_type=BlogInteraction.LIKE
    )
    
    # If it already existed, delete it (unlike)
    if not created:
        interaction.delete()
        messages.success(request, 'Post unliked!')
    else:
        messages.success(request, 'Post liked!')
    
    return redirect('blog_detail', pk=blog.pk)
