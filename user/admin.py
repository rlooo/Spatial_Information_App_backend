from django.contrib import admin

# Register your models here.
from user.models import Account

admin.site.register(Account)