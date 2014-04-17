from django.contrib import admin
from .models import Account, Topic, Comment, Like
# Register your models here.
admin.site.register(Account)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)
