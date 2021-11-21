from django.shortcuts import render

# Create your views here.

def display_table(request):
	return render(request,'dataapp/user_data.html')