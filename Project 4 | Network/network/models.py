from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about = models.TextField(max_length=160, blank=True)
    photo = models.URLField(max_length=2048, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)
    likes = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)

    def serialize(self):
        return {
            "author_name": self.author.username,
            "author_id": self.author.id,
            "comments": [comment for comment in self.comments.all()],
            "content": self. content,
            "id": self.id,
            "likes": [user.username for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "title": self.title
        }


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")


class FollowingList(models.Model):
    followees = models.ManyToManyField(User, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
