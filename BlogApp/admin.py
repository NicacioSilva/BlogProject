from django.contrib import admin
from .models import Post, Comment


# Every line writen here customizes the admin screen panel. You can do it
# one by one and seeing the results.

# Only this line creates a editable Post model on admin page:
# admin.site.register(Post)
#
# This decorator makes that class PostAdmin displayable according fields below.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # it controls which column will be displayed.
    list_display = ('title', 'slug', 'author', 'publish', 'status')

    # it generates a column list where you can sort by those fields.
    list_filter = ('status', 'created', 'publish', 'author')

    # it controls which fields will be searchable on the search bar.
    search_fields = ('title', 'body')

    # when you add new posts, the slug will be populated automatically,
    # when you write the title.
    prepopulated_fields = {'slug': ('title',)}

    # you don't have to write the author any more. Just click on search icon
    # and select some one.
    raw_id_fields = ('author',)

    # it controls the navigation links just below the search bar.
    date_hierarchy = 'publish'

    # it adds a little arrow that will order by status or publish.
    ordering = ('status', 'publish')


# every thing on this new class have the same properties and behaviors as described above.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
