from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from classrooms.models import (
	Classroom,
	RandomPerson
)


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.CharField(max_length=50, null=True, blank=True)
	username = models.CharField(max_length=50, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	
	classroom = models.ManyToManyField(Classroom, related_name='class+', blank=True)
	waiting = models.ManyToManyField(Classroom, related_name='approve', blank=True)
	picked = models.ManyToManyField(RandomPerson, related_name='randomperson', blank=True)
	
	
	def get_absolute_url(self):
		return reverse('users:users-home', kwargs={'slug': f'student{self.id}'})
	
	
	def __str__(self):
		return self.email


class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.CharField(max_length=150, null=True)
	username = models.CharField(max_length=50, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	
	classroom = models.ManyToManyField(Classroom, related_name='classroom', blank=True)
	picked = models.ManyToManyField(RandomPerson, related_name='randomperson_t', blank=True)
	
	
	def get_absolute_url(self):
		return reverse('users:users-home', kwargs={'slug': f'teacher{self.id}'})
	
	
	def __str__(self):
		return self.email
