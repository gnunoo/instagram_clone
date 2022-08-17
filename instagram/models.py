from django.db import models

# Create your models here.

class Feed(models.Model):

    content=models.TextField()
    Feed_image=models.TextField()
    email=models.EmailField(default='')
    like_count=models.IntegerField()



class Like(models.Model):
    feed_id=models.IntegerField()
    email=models.EmailField(default='')
    is_like=models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField()
    email = models.EmailField(default='')
    reply_content=models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField()
    email = models.EmailField(default='')
    is_marked=models.BooleanField(default=True)

