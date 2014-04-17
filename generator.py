#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
from ermiao.models import Account, Topic, Comment, User
from django.utils import timezone
import datetime, random

def create_user():
    for i in range(200):
        if not User.objects.filter(username='user{}'.format(i)):
            user = User.objects.create_user(username='user{}'.format(i), email='user{}@example.com'.format(i), password=i)
            user.save()

def create_account():
    for i in range(200):
        user = User.objects.get(username='user{}'.format(i))
        account = Account(user=user, pets=random.randrange(10))
        account.save()

def create_topic(days=0, hours=0):
    account = random.choice(Account.objects.all())
    likes = random.randrange(100)
    created = timezone.now() - datetime.timedelta(days=days, hours=hours)
    content = 'Topic created by {} on {}'.format(account, created)
    topic = Topic(account=account, content=content, created=created, likes=likes)
    topic.save()

def create_comment(days=0, hours=0):
    account = random.choice(Account.objects.all())
    topic = random.choice(Topic.objects.all())
    created = timezone.now() - datetime.timedelta(days=days, hours=hours)
    content = 'Comment created by {} on {}'.format(account, created)
    comment = Comment(account=account, topic=topic, content=content, created=created)
    comment.save()

def time_generator(days=5):
    return random.randrange(days), random.randrange(24)

if __name__ == '__main__':
    create_user()
    create_account()