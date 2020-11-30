from django.urls import path
from .views import (
	classes_list_view,
	class_detail_view,
	class_create_view,
	class_update_view,
	class_delete_view,
	class_generate_view,
	
	remove_student_view,
	ask_to_join_view,
	approve_student_view,
	
	save_picked_view,
)


app_name = 'classrooms'
urlpatterns = [
	path('', classes_list_view, name='classrooms-list'),
	path('create/', class_create_view, name='classroom-create'),
	path('<int:id>/', class_detail_view, name='classroom-detail'),
	path('<int:id>/update/', class_update_view, name='classroom-update'),
	path('<int:id>/delete/', class_delete_view, name='classroom-delete'),
	path('<int:id>/generate/', class_generate_view, name='classroom-generate'),
	
	path('remove/', remove_student_view, name='remove'),
	path('ask/', ask_to_join_view, name='ask'),
	path('approve/', approve_student_view, name='approve'),
	
	path('picked/', save_picked_view, name='picked'),
]
