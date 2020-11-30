from django.contrib import admin

from .models import Classroom
from .models import RandomPerson


admin.site.register(Classroom)
admin.site.register(RandomPerson)
