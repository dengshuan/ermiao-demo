from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    pets = models.IntegerField()
    def __unicode__(self):
        return self.user.username

class Topic(models.Model):
    account = models.ForeignKey(Account)
    content = models.CharField(max_length=200)
    created = models.DateTimeField()
    # likes = models.IntegerField(default=0)

    def was_published_recently(self):
        return self.created <= timezone.now() - datetime.timedelta(days=1)

    def __unicode__(self):
        return self.content


class Comment(models.Model):
    account = models.ForeignKey(Account)
    topic = models.ForeignKey(Topic)
    content = models.CharField(max_length=200)
    created = models.DateTimeField()

    def was_published_recently(self):
        return self.created <= timezone.now() - datetime.timedelta(days=1)    

    def __unicode__(self):
        return self.content

class Like(models.Model):
    topic = models.ForeignKey(Topic)
    account = models.ForeignKey(Account)
    clicked = models.DateTimeField()
