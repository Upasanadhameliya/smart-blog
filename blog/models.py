from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to='blogs/',
        blank=True,
        null=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_like_count(self):
        """Get the total number of likes for this blog."""
        from interactions.models import BlogInteraction
        return BlogInteraction.objects.filter(
            blog=self,
            interaction_type=BlogInteraction.LIKE
        ).count()
    
    def get_view_count(self):
        """Get the total number of views for this blog."""
        from interactions.models import BlogInteraction
        return BlogInteraction.objects.filter(
            blog=self,
            interaction_type=BlogInteraction.VIEW
        ).count()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


