from django.shortcuts import render, get_object_or_404
from blog.models import Post


# Create your views here.


def home(request):
    return render(request, "blog/index.html")


def blog(request):
    posts = Post.published.all()
    return render(request, "blog/blog.html", {'posts': posts})


def post(request, post_id):
    each_post = get_object_or_404(Post, post_id=post_id, status=Post.Status.PUBLISHED)
    return render(request, "blog/post.html", {'post': each_post})

