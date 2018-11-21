from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            'user',
            'content',
            'image'
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1000:
            raise forms.ValidationError("Content is too long")
        return content

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content is "":
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise forms.ValidationError('Content and Image field are required!')
        return super().clean(*args, **kwargs)
