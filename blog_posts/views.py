from django.shortcuts import render

# Create your views here.
# blog/views.py
from django.shortcuts import render
from .models import BlogPost
from .utils import fetch_articles_and_create_posts

def blogpage(request):
    fetch_articles_and_create_posts()
    posts = BlogPost.objects.all().order_by('-published_at')
    return render(request, 'blogposts.html', {'posts': posts})

