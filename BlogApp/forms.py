from django import forms


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
