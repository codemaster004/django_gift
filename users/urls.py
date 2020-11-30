from django.urls import path
from .views import (
	home_view,
	profile_update_view,
	profile_delete_view
)


app_name = 'users'
urlpatterns = [
	path('<slug:slug>/', home_view, name='users-home'),
	path('<slug:slug>/update/', profile_update_view, name='profile-update'),
	path('<slug:slug>/delete/', profile_delete_view, name='profile-delete'),
]
