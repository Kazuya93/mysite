from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def index(request):
	next = request.GET.get('next')
	return render(request, 'index.html', {'next':next})

def register_page(request):
	return render(request, 'register.html')

def user_login(request):
	redirect_to = request.GET.get('next', '/main')
	username = request.POST.get('username')
	password = request.POST.get('password')
	content = {}
	user = authenticate(username=username, password=password)
	if user is None:
		content['msg'] = 'Wrong username or password!'
		return render(request, 'index.html', content)
	login(request, user)
	return redirect(redirect_to)

def register(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	email = request.POST.get('email')
	content = {}
	if User.objects.filter(username=username).exists():
		content['msg'] = "Username existed!"
		return render(request,'register.html',content)
	elif User.objects.filter(email=email).exists():
		content['msg'] = "Email existed!"
		return render(request,'register.html',content)
	user = User.objects.create_user(username, email, password)
	user.first_name = firstname
	user.last_name = lastname
	user.save()
	content['msg'] = "Register Success!"
	return render(request,'index.html', content)

@login_required
def main_page(request):
 	return render(request, 'main.html',{'name':request.user.first_name})

@login_required
def user_logout(request):
	logout(request)
	content = {}
	content['msg'] = 'Successully log out'
	return render(request, 'index.html', content)

@login_required
def create_event(request):
	return render(request, 'event.html')

