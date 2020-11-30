# Generated by Django 3.1 on 2020-11-28 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0002_classroom_creator'),
        ('users', '0004_auto_20201128_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.AddField(
            model_name='student',
            name='classroom',
            field=models.ManyToManyField(blank=True, related_name='_student_classroom_+', to='classrooms.Classroom'),
        ),
    ]
