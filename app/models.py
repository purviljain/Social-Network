from django.db import models
from django.utils import timezone
from signup.models import Profile
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    post_pic = models.FileField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta():
        ordering = ['-date_created']

class Comment(models.Model):
    post = models.ForeignKey("app.Post", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    class Meta():
        ordering = ["-date_created"]

# class Like(models.Model):
#     post = models.ForeignKey("app.Post", related_name="comments")
#     user = models.ForeignKey("auth.User")
#     like = models.
#     date_created = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.comment
#
#     class Meta():
#         ordering = ["-date_created"]
