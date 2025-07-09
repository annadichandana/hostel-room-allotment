from django.urls import path
from .import views

urlpatterns = [
    path('',views.base,name='base'),
    path('homepage/', views.members, name="members"),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('view-students/', views.view_students, name='view_students'),
    path('view-rooms/', views.view_rooms, name='view_rooms'),
    path('add-room/', views.add_room, name='add_room'),
    path('allocate-room/', views.allocate_room, name='allocate_room'),
    path('logout/', views.logout_view, name='logout'),
    path('view_details/',views.view_details,name='view_details'),
    path('forgot/',views.forgot,name='forgot'),
    path('room-chart/', views.room_chart, name='room_chart'),
    path('room_overview/', views.room_overview, name='room_overview'),
    path('room_info/', views.room_info, name='room_info'),
    path('manage-students/', views.manage_students, name='manage_students'),  
    path('edit-student/', views.edit_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]