from django.db import models

from blog.models import Blog
from accounts.models import User

# Create your models here.

class BlogInteraction(models.Model):
    VIEW = 'view'
    LIKE = 'like'

    INTERACTION_CHOICES = (
        (VIEW, 'View'),
        (LIKE, 'Like'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['blog']),
        ]
        unique_together = ('user', 'blog', 'interaction_type')

    def __str__(self):
        return f"{self.user} {self.interaction_type} {self.blog}"

