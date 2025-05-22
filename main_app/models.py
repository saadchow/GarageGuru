from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class UserDescription(models.Model):
    description = models.TextField(max_length=10000, blank=True, default='No User Bio')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserPhoto(models.Model):
    image = CloudinaryField('image', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for user_id: {self.user_id} @{self.image.url}"

class Post(models.Model):
    description = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-description']

class Photo(models.Model):
    image = CloudinaryField('image')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.image.url}"

class Comment(models.Model):
    comment = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
