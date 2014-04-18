from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import random, datetime
from .models import Account, Topic, Comment, Like

# Create your views here.
class IndexView(ListView):
    template_name = 'ermiao/index.djhtml'
    def get_latest_topics(self):
        topics = Topic.objects.all()
        latest = [t for t in topics if t.was_published_recently()]
        outdated = [t for t in topics if not t.was_published_recently()]
        for item in latest:
            item.weight = 0
            if item.like_set.count > 0:
                item.weight = item.weight + 1.0
            for comment in item.comment_set.all():
                if comment.account.pets > 0:
                    item.weight = item.weight + 1.5
                else:
                    item.weight = item.weight + 1.0
        top100 = sorted(latest, key=lambda item: item.weight)[-100:]

        candidates1, candidates2 = [], []
        for item in outdated:
            if item.account.user.last_login <= timezone.now() - datetime.timedelta(days=2):
                candidates1.append(item)
        for candidate in candidates1:
            candidate.latest_comments = 0
            for c in candidate.comment_set.all():
                if c.was_published_recently():
                    candidate.latest_comments += 1
            if candidate.like_set.count > 2 and candidate.latest_comments > 1:
                candidates2.append(candidate)
        random15 = []
        if len(candidates2) <= 15:
            random15 = candidates2
        else:
            for i in range(15):
                r = random.choice(candidates2)
                random15.append(r)
                candidates2.remove(r)

        to_be_shown = top100 + random15
        return to_be_shown

    def last_operated(self, item):
        t1 = item.account.user.last_login
        if item.comment_set.all():
            t2 = item.comment_set.latest('created').created
        else:                   # topic has no comments
            t2 = item.created
        if item.like_set.all():
            t3 = item.like_set.latest('clicked').clicked
        else:
            t3 = item.created
        return max(t1, t2, t3)

    def get_queryset(self):
        items = self.get_latest_topics()
        for item in items:
            item.last_operated = self.last_operated(item)
        items = sorted(items, key=lambda item: item.last_operated, reverse=True)
        return items


def create_topic(request):
    if request.method == 'POST':
        username = request.POST['username']
        content = request.POST['content']
        account = Account.objects.get(user__username=username)
        created = timezone.now()
        t = Topic(account=account, content=content, created=created, likes=0)
        t.save()
        return redirect(reverse('ermiao:index'))
    return redirect(reverse('ermiao:index'))

def add_comment(request):
    if request.method == 'POST':
        username = request.POST['username']
        content = request.POST['content']
        topic_id = request.POST['topic']
        account = Account.objects.get(user__username=username)
        topic = Topic.objects.get(pk=topic_id)
        created = timezone.now()
        c = Comment(account=account, topic=topic, content=content, created=created)
        c.save()
        return redirect(reverse('ermiao:index'))
    return redirect(reverse('ermiao:index'))

def tag_like(request):
    if request.method == 'POST':
        username = request.POST['username']
        topic_id = request.POST['topic']
        account = Account.objects.get(user__username=username)
        topic = Topic.objects.get(pk=topic_id)
        clicked = timezone.now()
        like = Like(account=account, topic=topic, clicked=clicked)
        like.save()
        return redirect(reverse('ermiao:index'))
    return redirect(reverse('ermiao:index'))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('ermiao:index'))
    return redirect(reverse('ermiao:index'))

def logout_view(request):
    logout(request)
    return redirect(reverse('ermiao:index'))
