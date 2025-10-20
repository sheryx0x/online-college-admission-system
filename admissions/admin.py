from django.contrib import admin
from .models import  Program, College,MeritList,Profile,Announcement,FAApplication,BSApplication,FSCApplication

admin.site.register(Profile)
admin.site.register(FAApplication)
admin.site.register(BSApplication)
admin.site.register(FSCApplication)
admin.site.register(College)
admin.site.register(Program)
admin.site.register(MeritList)
admin.site.register(Announcement)
