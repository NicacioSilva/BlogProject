from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    # it is querying all published posts from db
    queryset = Post.published.all()
    # it specify the context variable as 'posts'.
    context_object_name = 'posts'
    # it'll limit number of posts in 3. It's called pagination.
    paginate_by = 3
    # and then render this page using list.html
    template_name = 'BlogApp/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'BlogApp/post/detail.html',
                  {'post': post})
