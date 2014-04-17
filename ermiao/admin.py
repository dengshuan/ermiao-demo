from django.contrib import admin
from .models import Account, Topic, Comment
# Register your models here.
admin.site.register(Account)
admin.site.register(Topic)
admin.site.register(Comment)
