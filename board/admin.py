from django.contrib import admin

# Register your models here.
from board.models import PutOut, LookFor, ApplySpace, BldRgstService, QnA, Notice, BuildingImage

admin.site.register(PutOut)
admin.site.register(LookFor)
admin.site.register(ApplySpace)
admin.site.register(BldRgstService)
admin.site.register(QnA)
admin.site.register(Notice)
admin.site.register(BuildingImage)