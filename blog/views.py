from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def home(request):
    return render(request, "blog/index.html")


def blog(request, tag_slug=None):
    posts = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

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
    return render(request, "blog/blog.html", {'posts': posts_list, 'tag': tag})


# class BlogListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/blog.html'


def send_email(request, post_id):
    each_post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form passed validation
            cd = form.cleaned_data
            # ....send email
            post_url = request.build_absolute_uri(
                each_post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read " \
                      f"{each_post.title}"
            message = f"Read {each_post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post.html', {'post': each_post, 'form': form, 'sent': sent})


def post(request,  post_id, year, month, day, slug):
    # retrieving the post
    each_post = get_object_or_404(Post,
                                  status=Post.Status.PUBLISHED,
                                  id=post_id,
                                  slug=slug,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)

    # List of all active comments for this post
    comments = each_post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = each_post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=each_post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, "blog/post.html", {'post': each_post,
                                              'comments': comments,
                                              'form': form,
                                              'similar_posts': similar_posts,
                                              })


@require_POST
def post_comment(request,  post_id, year, month, day, slug):
    # each_post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    each_post = get_object_or_404(Post,
                                  status=Post.Status.PUBLISHED,
                                  id=post_id,
                                  slug=slug,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)

    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = each_post
        # save the comment to the database
        comment.save()
        return redirect('blog:post', each_post.id, each_post.publish.year,
                        each_post.publish.month,
                        each_post.publish.day,
                        each_post.slug,
                        )

    return render(request, 'blog/post.html', {'post': each_post,
                                              'form': form,
                                              'comment': comment
                                              })

