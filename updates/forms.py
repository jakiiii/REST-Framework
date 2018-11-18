from django import forms

from .models import Update as UpdateModel


class UpdateModelFrom(forms.ModelForm):
    class Meta:
        model = UpdateModel
        fields = [
            'user',
            'title',
            'image',
            'content'
        ]

    def clean(self, *args, **kwargs):
        title = self.cleaned_data.get('title' or None)
        image = self.cleaned_data.get('image' or None)
        content = self.cleaned_data.get('content' or None)
        if title is None and content is None:
            raise forms.ValidationError('Title and content is required!')
        return super().clean(*args, **kwargs)
