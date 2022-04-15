from django.contrib import admin

# Register your models here.
from board.models import Address, Board

admin.site.register(Address)
admin.site.register(Board)