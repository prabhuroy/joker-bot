from django.shortcuts import render
from .models import *
# Create your views here.

def display_table(request):
	objects_list = UserData.objects.all()
	return render(request,'dataapp/user_data.html',{'objects_list':objects_list})