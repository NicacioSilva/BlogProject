from decouple import config
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


# class PostListView(ListView):
#     # it is querying all published posts from db
#     queryset = Post.published.all()
#     # it specify the context variable as 'posts'.
#     context_object_name = 'posts'
#     # it'll limit number of posts in 3. It's called pagination.
#     paginate_by = 3
#     # and then render this page using list.html
#     template_name = 'BlogApp/post/list.html'

def post_list(request, tag_slug=None):
    # Get a list of all published posts
    published_posts = Post.published.all()
    # create a tag variable to use it inside of the if scope below
    tag = None

    if tag_slug:
        # if there's some thing in tag_slug, it'll extract to tag variable
        tag = get_object_or_404(Tag, slug=tag_slug)
        # and let's filter published_post's list by that tag
        published_posts = published_posts.filter(tags__in=[tag])

    # it determinates the quantity of posts will be displayed
    paginator = Paginator(published_posts, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'BlogApp/post/list.html', {'page': page,
                                                      'posts': posts,
                                                      'tag': tag})


def post_detail(request, year, month, day, post):
    # This post_detail method is about to properly display in detail a single post
    # and, of course, its other characteristics as comments and a form to write new
    # comments.

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Let's retrieve all the active comments for this post
    comments = post.comments.filter(active=True)

    # We satiate a new_comment now to deal it later
    new_comment = None

    # Now we handle GET and POST methods
    if request.method == 'POST':
        # It's suppose that a comment was posted, so let's extract its data
        comment_form = CommentForm(data=request.POST)

        # and we need to now if its data is valid and what to if its not valid
        if comment_form.is_valid():
            # extract data from comment_form to new_comment variable
            # commit=False will assure it's not save to database yet
            new_comment = comment_form.save(commit=False)
            # assure this comment will belongs to the post that user have commented
            new_comment.post = post
            # and finally save it in the database
            new_comment.save()
    else:
        # if it's only a GET method, it's only to show the form, so:
        comment_form = CommentForm()

    # Now we have all variable's setup in a properly way, let's rendering it in the html through render method
    return render(request,
                  'BlogApp/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


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
