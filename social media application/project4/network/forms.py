from django import forms
from django.forms import ModelForm
from .models import Posts, FFowers, Comments
from datetime import datetime
from django.shortcuts import get_object_or_404

class CreatePost(ModelForm):
    class Meta:
        model = Posts
        fields = ['name', 'picture_link']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.request.user
        instance.owner_name = self.request.user.username
        instance.likes = 0
        instance.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if commit:
            instance.save()
        return instance

class AddComments(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.post_id = kwargs.pop('post_id', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.request.user
        post = get_object_or_404(Posts, id=self.post_id)  
        instance.post_id = post
        if commit:
            instance.save()
        return instance
    

    

 