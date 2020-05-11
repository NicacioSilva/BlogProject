from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Now lets create a manager, this manager allow you
# to retrieve posts using like: Post.published.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# This is a model data for blog posts
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # It'll be a VARCHAR for the posts titles
    title = models.CharField(max_length=250)

    # slog's a Django feature for generate beautiful urls
    # using its publishing dates and they will be unique
    # and it's Django that will assure it
    # even if they was published same date.
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # It'll create a separated table for authors, it's a relation
    # of many-to-one. The on_delete plus .CASCADE says when you
    # delete an user all its related posts will be also deleted.
    # related_name means you can select user by blog_posts and
    # vice versa.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    # It's body's post.
    body = models.TextField()

    # It uses Django's timezone.now() as default value
    # indicating when post was published.
    publish = models.DateTimeField(default=timezone.now)

    # Since you use auto_now_add, the date will be saved automatically
    # when creating an object
    created = models.DateTimeField(auto_now_add=True)

    # The date will be updated automatically when you save an object.
    updated = models.DateTimeField(auto_now=True)

    # You can only choose STATUS_CHOICES who are pre-defined.
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    # This is the default manager.
    objects = models.Manager()

    # This is a custom manager.
    published = PublishedManager()

    # By adding this tags obj, it allows you to add, retrieve and remove tags from Post objects.
    tags = TaggableManager()

    # This class contains meta data. When you use the negative prefix
    # means that once you query the database it will sort by descending
    # order all the publish fields.
    class Meta:
        ordering = ('-publish',)

    # It makes representation human-readable. It'll be useful in
    # the administration site.
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('BlogApp:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    # This is comment's class

    # - Post's ForeignKey is many-to-one relation, it means that a post
    # will have many comments, but every comments belongs to one post only.
    # - The on_delete=models.CASCADE, means once you delete a post, all
    # the comments that belongs to that post will be also deleted.
    # - The related_name='comments' gives the power to do:
    # post.comments.all() and retrieves all the comments of that post.
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    # This EmailField automatically validates emails.
    email = models.EmailField()
    body = models.TextField()
    # This auto_now_add creates a read only field, after it was created.
    created = models.DateTimeField(auto_now_add=True)
    # This auto_now create a field that can by updated once it changes.
    updated = models.DateTimeField(auto_now=True)
    # You can set default as True or False, what turns comments
    # possible to be activate or deactivated.
    active = models.BooleanField(default=True)

    # It's giving to Comment the property of sort by 'created'.
    class Meta:
        ordering = ('created',)

    # This's what'll be printed, when you print a comment obj.
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
