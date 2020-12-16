from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

try:
	from django.utils import simplejson as json
except ImportError:
	import json

from .models import (
	Classroom,
	RandomPerson
)
from users.models import (
	Student,
	Teacher
)

import random


@login_required(login_url='signin')
def class_create_view(request):
	
	base_data = get_my_classes(request)
	
	if base_data['user_type'] != 'teacher':
		redirect('/')
	
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.user.email
		
		exists = Classroom.objects.filter(name__exact=name).first()
		print(exists)
		if exists is None:
			new_classroom = Classroom.objects.create(creator=email, name=name)
			teacher = Teacher.objects.get(email__exact=email)
		
			teacher.classroom.add(new_classroom)
		
			return redirect(f'/classes/{new_classroom.id}/')
		else:
			messages.info(request, 'Class with this name already exists, plese pick a different one')
	
	context = {
		'context': base_data,
	}
	
	return render(request, "classrooms/classroom_create.html", context)


def get_my_classes(request):
	username = request.user.username
	email = request.user.email
	
	user_type = 'student'
	user = Student.objects.filter(email__exact=email).first()
	if user is None:
		user_type = 'teacher'
		user = Teacher.objects.filter(email__exact=email).first()
	
	classes = []
	if user is not None:
		classes = user.classroom.all()
	
	context = {
		'base_user': user,
		'username': username,
		'classes': classes,
		'user_type': user_type
	}
	
	return context


@login_required(login_url='signin')
def classes_list_view(request):
	query = request.GET.get('search_class')
	
	classes = Classroom.objects.filter(name__icontains=query)
	
	email = request.user.email
	user = Student.objects.filter(email__exact=email).first()
	if user is None:
		user = Teacher.objects.filter(email__exact=email).first()
	
	waiting = user.waiting.all()
	my_classes = user.classroom.all()
	
	base_data = get_my_classes(request)
	
	context = {
		'classes_find': classes,
		'waiting': waiting,
		'my_classes': my_classes,
		'user_email': request.user.email,
		'context': base_data
	}
	
	return render(request, "classrooms/classroom_list.html", context)


@login_required(login_url='signin')
def class_detail_view(request, id):
	obj = get_object_or_404(Classroom, id=id)
	
	students = Student.objects.filter(classroom__name=obj.name)
	teacher = Teacher.objects.filter(classroom__name=obj.name).first()
	
	students = [student for student in students]
	students.append(teacher)
	
	email = request.user.email
	
	user = Student.objects.filter(email__exact=email).first()
	if user is None:
		user = Teacher.objects.filter(email__exact=email).first()
		
	picked_person = user.picked.filter(class_name=obj.name).first()
	
	base_data = get_my_classes(request)
	
	if not (user in students):
		redirect('/classes/')
	
	context = {
		'object': obj,
		'students': sorted(students, key=lambda x: x.username),
		'teacher': teacher,
		'context': base_data,
		'picked_person': picked_person,
	}
	return render(request, "classrooms/classroom_detail.html", context)


@login_required(login_url='signin')
def class_update_view(request, id):
	obj = get_object_or_404(Classroom, id=id)
	
	base_data = get_my_classes(request)
	
	if base_data['user_type'] != 'teacher':
		redirect('/')
	
	students = Student.objects.filter(classroom__name=obj.name)
	waiting = Student.objects.filter(waiting__name=obj.name)
	teacher = Teacher.objects.filter(classroom__name=obj.name).first()
	
	if request.method == 'POST':
		name = request.POST.get('name')
		
		obj.name = name
		obj.save()
		
		return redirect(f'/classes/{obj.id}')
	
	context = {
		'object': obj,
		'students': students,
		'teacher': teacher,
		'waiting': waiting,
		'context': base_data
	}
	return render(request, "classrooms/classroom_update.html", context)


@login_required(login_url='signin')
def class_delete_view(request, id):
	
	base_data = get_my_classes(request)
	
	if base_data['user_type'] != 'teacher':
		redirect('/')
	
	obj = get_object_or_404(Classroom, id=id)
	if request.method == "POST":
		sudents = Student.objects.filter(classroom__name=obj.name)
		for student in sudents:
			student.classroom.remove(obj)
		obj.delete()
		
		email = request.user.email
		
		user_type = 'student'
		user = Student.objects.filter(email__exact=email).first()
		if user is None:
			user_type = 'teacher'
			user = Teacher.objects.filter(email__exact=email).first()
		
		return redirect(f'/user/{user_type}{user.id}/')
	
	context = {
		"object": obj,
		'context': base_data
	}
	return render(request, "classrooms/classroom_delete.html", context)


@login_required(login_url='signin')
def class_generate_view(request, id):
	obj = get_object_or_404(Classroom, id=id)
	
	base_data = get_my_classes(request)
	
	if base_data['user_type'] != 'teacher':
		redirect('/')
	
	students = Student.objects.filter(classroom__name=obj.name)
	teacher = Teacher.objects.filter(classroom__name=obj.name).first()
	
	users = [student for student in students]
	users.append(teacher)
	new_users = users[:]
			
	if len(users) != 1:
		not_shuffled = True
		while not_shuffled:
			random.shuffle(new_users)
			
			value = False
			for user_index in range(len(new_users)):
				if new_users[user_index] == users[user_index]:
					value = True
			not_shuffled = value
	
	context = {
		'object': obj,
		'users': users,
		'picked_users': new_users,
		'context': base_data,
	}
	return render(request, "classrooms/classroom_generate.html", context)


@login_required
@require_POST
def save_picked_view(request):
	if request.method == 'POST':
		classroom_id = request.POST.get('classroom', None)
		users = request.POST.getlist('users[]', None)
		picked = request.POST.getlist('picked[]', None)
		
		classroom = Classroom.objects.get(pk=classroom_id)
		
		for user_index in range(len(users)):
			username = users[user_index]
			picked_name = picked[user_index]
			
			user = Student.objects.filter(username__exact=username).first()
			if user is None:
				user = Teacher.objects.filter(username__exact=username).first()
			
			picked_person = RandomPerson.objects.create(class_name=classroom.name, user_name=username, picked_name=picked_name)
			
			user.picked.add(picked_person)
			
		
		classroom = Classroom.objects.get(pk=classroom_id)
		

	ctx = {}
	return HttpResponse(json.dumps(ctx), content_type='application/json')
	

@login_required
@require_POST
def remove_student_view(request):
	if request.method == 'POST':
		student_id = request.POST.get('student', None)
		classroom_id = request.POST.get('classroom', None)
		
		student = Student.objects.get(pk=student_id)
		classroom = Classroom.objects.get(pk=classroom_id)
		
		student.classroom.remove(classroom)

	ctx = {}
	return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
@require_POST
def ask_to_join_view(request):
	if request.method == 'POST':
		student_email = request.POST.get('student', None)
		classroom_id = request.POST.get('classroom', None)
		
		student = Student.objects.get(email=student_email)
		classroom = Classroom.objects.get(pk=classroom_id)
		
		student.waiting.add(classroom)

	ctx = {}
	return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
@require_POST
def approve_student_view(request):
	if request.method == 'POST':
		student_id = request.POST.get('student', None)
		classroom_id = request.POST.get('classroom', None)
		
		student = Student.objects.get(pk=student_id)
		classroom = Classroom.objects.get(pk=classroom_id)
		
		student.waiting.remove(classroom)
		student.classroom.add(classroom)

	ctx = {}
	return HttpResponse(json.dumps(ctx), content_type='application/json')
