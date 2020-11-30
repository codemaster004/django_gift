from django.db import models
from django.urls import reverse


class Classroom(models.Model):
	creator = models.CharField(max_length=150, null=True)
	name = models.CharField(max_length=30, unique=True)
	
	
	def get_absolute_url(self):
		return reverse("classrooms:classroom-detail", kwargs={"id": self.id})
	
	
	def __str__(self):
		return self.name

class RandomPerson(models.Model):
	class_name = models.CharField(max_length=150, null=True)
	user_name = models.CharField(max_length=150, null=True)
	picked_name = models.CharField(max_length=150, null=True)
	
	def __str__(self):
		return self.picked_name
