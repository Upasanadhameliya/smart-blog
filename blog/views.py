from django.shortcuts import render
from .models import Blog

def home(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blog/home.html', context)
