from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django import forms

class UserDescription(models.Model):
    description = models.TextField(max_length=10000, blank=True, default='No User Bio')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserPhoto(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for user_id: {self.user_id} @{self.url}"



class Post(models.Model):
    description = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def user_like_list (post_id):
        user_list = []
        idx = 0
        for x in Like.objects.filter(post_id=post_id):
            idx_user = (Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
            user_list.append(User.objects.filter(id=idx_user).values('username')[0]['username'])
            idx += 1
        return user_list
    def like_list_generator (post_id):
        like_list = []
        idx = 0
        for x in Like.objects.filter(post_id=post_id):
            like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
            idx += 1
        return like_list
    class Meta:
        ordering = ['-description']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ["description"]

class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["url"]

class Comment(models.Model):
    comment = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like_list_generator (post_id):
        like_list = []
        idx = 0
        for x in Like.objects.filter(post_id=post_id):
            like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
            idx += 1
        return like_list

class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
   

