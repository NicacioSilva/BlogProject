from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # it ensures a max length for the name.
    name = forms.CharField(max_length=25)
    # it automatically checks if it's a valid email.
    email = forms.EmailField()
    to = forms.EmailField()
    # that False means comments are optional.
    # Textarea will shows it no only as input text, but also as <textarea> HTML element.
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


# Instead of using forms.Form to build forms,
# as we already have models for comments, we can reuse them
# and create this forms thought those comments models by using
# forms.ModelForm.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # All we've to do is specify what models we want to reuse,
        # listing them in this fields tuple.
        # Then Django'll create a form with those exactly fields,
        # and each one of them will inherit its validation properties,
        # like email, size, etc. And that's freaking cool =D
        fields = ('name', 'email', 'body')
