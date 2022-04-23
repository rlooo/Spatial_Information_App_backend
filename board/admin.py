from django.contrib import admin

# Register your models here.
from board.models import PutOutBoard, LookForBoard

admin.site.register(PutOutBoard)
admin.site.register(LookForBoard)