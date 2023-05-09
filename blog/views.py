from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def home(request):
    return render(request, "blog/index.html")


def blog(request):
    posts = Post.published.all()
    # Pagination with three posts per page.
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts_list = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer the first page is viewed
        posts_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range
        posts_list = paginator.page(paginator.num_pages)
    return render(request, "blog/blog.html", {'posts': posts_list})


# class BlogListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/blog.html'


def post(request,  post_id, year, month, day, slug):
    each_post = get_object_or_404(Post,
                                  status=Post.Status.PUBLISHED,
                                  id=post_id,
                                  slug=slug,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)
    return render(request, "blog/post.html", {'post': each_post})

