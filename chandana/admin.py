from django.contrib import admin
from .models import student,rooms,RoomAllocation
admin.site.register(student)
admin.site.register(rooms)
admin.site.register(RoomAllocation)