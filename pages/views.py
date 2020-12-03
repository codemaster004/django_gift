from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm
from users.models import (
	Teacher,
	Student
)


def signup_page(request):
	context = {}
	
	form = CreateUserForm()
	
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			email = request.POST.get('email')
			username = request.POST.get('username')
			password = request.POST.get('password1')
			teacher_bool = request.POST.get('user_type')
			
			if User.objects.filter(email=email).exists():
				messages.error(request, 'User with this email alredy exists')
				
				context['form'] = form
				return render(request, 'pages/signup.html', context)
			
			user = User.objects.create_user(username=username, email=email)
			user.set_password(password)
			user.save()
			
			if teacher_bool:
				new_teacher = Teacher.objects.create(
					user=user,
					email=email,
					username=username
				)
				new_teacher.save()
			else:
				new_student = Student.objects.create(
					user=user,
					email=email,
					username=username
				)
				new_student.save()
			
			messages.success(request, 'Your account was created Successfully')
			
			return redirect('signin')
	
	context['form'] = form
	
	return render(request, 'pages/signup.html', context)


def login_page(request):
	if request.method == 'POST': 
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			
			email = user.email
			
			user_type = 'student'
			user = Student.objects.filter(email__exact=email).first()
			if user is None:
				user_type = 'teacher'
				user = Teacher.objects.filter(email__exact=email).first()
			
			return redirect(f'/user/{user_type}{user.id}/')
		else:
			messages.info(request, 'Username or Password is incorrect')
			
	context = {}
	return render(request, 'pages/signin.html', context)


def logout_page(request):
	logout(request)
	return redirect('signin')


def landing_page(request):
	
	context = {}
	
	return render(request, 'pages/landing.html', context)
