from django.contrib import admin
from .models import *
# Register your models here.
class VisitorAdmin(admin.ModelAdmin):
    list_display=['name','email']
admin.site.register(Visitor_data,VisitorAdmin)