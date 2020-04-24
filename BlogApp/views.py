from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    # it is querying all published posts from db
    object_list = Post.published.all()
    # it'll limit number of posts in 3
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        # try go to its page.
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if it's not an int, go first page.
        posts = paginator.page(1)
    except EmptyPage:
        # if it's too big number, go last page.
        posts = paginator.page(paginator.num_pages)
    # and then render this page using list.html
    return render(request,
                  'BlogApp/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'BlogApp/post/detail.html',
                  {'post': post})
