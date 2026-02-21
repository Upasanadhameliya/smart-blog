from django.contrib import admin
from .models import BlogInteraction

@admin.register(BlogInteraction)
class BlogInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'interaction_type', 'created_at')
    list_filter = ('interaction_type', 'created_at')
    search_fields = ('user__username', 'blog__title')
    ordering = ('-created_at',)

