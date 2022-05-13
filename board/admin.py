from django.contrib import admin

# Register your models here.
from board.models import PutOut, LookFor, GisBuildingService, ApplySpace, BldRgstService

admin.site.register(PutOut)
admin.site.register(LookFor)
admin.site.register(ApplySpace)
admin.site.register(GisBuildingService)
admin.site.register(BldRgstService)