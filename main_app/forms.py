from django import forms
from .models import Post, Photo, UserPhoto, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ["description"]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image"]

class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
