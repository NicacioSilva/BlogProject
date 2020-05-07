from decouple import config
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


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


def post_share(request, post_id):
    # This method takes the request obj and retrieves a post by its id on post_id's variable.
    # If request's a POST, then it sends a email using form's information.
    # If request's a GET, it just show an empty form.

    # we use get_object_or_404 to assure that the requested post is PUBLISHED.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form's content was submitted to form variable
        form = EmailPostForm(request.POST)
        # here form's content is validated by .isvalid() method.
        if form.is_valid():
            # form's content is retrieved to cd variable.
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"

            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"

            send_mail(subject, message, config('EMAIL_HOST_USER'), [cd['to']])

            sent = True

    else:
        # if ti's a GET request, then create a new form instance which will be used on render.
        form = EmailPostForm()

    # what ever happened above, it will return an answer inside form and post
    # which will be rendered over here to share.html.
    return render(request, 'BlogApp/post/share.html', {'post': post,
                                                       'form': form,
                                                       'sent': sent})
