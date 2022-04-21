from django.contrib import admin

# Register your models here.
from board.models import Address, PutOutBoard, LookForBoard

admin.site.register(Address)
admin.site.register(PutOutBoard)
admin.site.register(LookForBoard)