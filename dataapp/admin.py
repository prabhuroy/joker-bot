from django.contrib import admin
from .models import *
# Register your models here.
class UserDataList(admin.ModelAdmin):
    list_display = ['userid', "user_name","fat_count","dumb_count","stupid_count"]

    class Meta:
        Model = UserData
admin.site.register(UserData,UserDataList)