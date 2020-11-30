from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from classrooms.views import get_my_classes
from .models import (
	Teacher,
	Student
)


@login_required(login_url='signin')
def home_view(request, slug):
	user = None
	
	user_id = int(''.join(filter(str.isdigit, slug)))
	
	if 'student' in slug:
		user = Student.objects.get(id=user_id)
	else:
		user = Teacher.objects.get(id=user_id)
	
	base_data = get_my_classes(request)
	
	email = user.email
	username = user.username
	bio = user.bio
	
	context = {
		'username': username,
		'email': email,
		'bio': bio,
		'slug': slug,
		'context': base_data,
	}
	
	return render(request, 'users/home.html', context)


@login_required(login_url='signin')
def profile_update_view(request, slug):
	user = None
	
	user_id = int(''.join(filter(str.isdigit, slug)))
	
	if 'student' in slug:
		user = Student.objects.get(id=user_id)
	else:
		user = Teacher.objects.get(id=user_id)
	
	email = request.user.email
	username = ''
	bio = ''
	
	if request.method == 'POST':
		new_name = request.POST.get('username')
		new_bio = request.POST.get('bio')
		
		user.bio = new_bio
		user.username = new_name
		
		user.save()
		
		return redirect(f'/user/{slug}/')
	elif request.method == 'GET':
		username = user.username
		bio = user.bio
	
	base_data = get_my_classes(request)
	
	context = {
		'email': email,
		'username': username,
		'bio': bio,
		'slug': slug,
		'context': base_data,
	}
	
	return render(request, 'users/profile_update.html', context)


@login_required(login_url='signin')
def profile_delete_view(request, slug):
	user = None
	
	user_id = int(''.join(filter(str.isdigit, slug)))
	
	if 'student' in slug:
		user = Student.objects.get(id=user_id)
	else:
		user = Teacher.objects.get(id=user_id)
	
	if request.method == "POST":
		email = request.user.email
		user = User.objects.get(email=em)
		
		user.delete()
		return redirect('/')
	
	base_data = get_my_classes(request)
	
	context = {
		'user': user,
		'context': base_data,
	}
	return render(request, 'users/profile_delete.html', context)
