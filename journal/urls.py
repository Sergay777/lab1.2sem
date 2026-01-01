from django.urls import path
from . import views

urlpatterns = [
    # Общие маршруты
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('contacts/', views.contacts, name="contacts"),
    path('add/', views.add_attendance, name='attendance_add'),
    path('profile/', views.profile, name='profile'),
    path('teacher/', views.teacher_panel, name='teacher_panel'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('stats/', views.attendance_stats, name='attendance_stats'),
    path('my-attendance/', views.my_attendance, name='my_attendance'),
    path('group-stats/', views.group_stats, name='group_stats'),

    # Маршруты для преподавателя (Lab 3)
    path("teacher/groups/", views.GroupListView.as_view(), name="teacher-groups"),
    path("teacher/group/<int:group_id>/students/", views.StudentListView.as_view(), name="teacher-group-students"),
    path("teacher/group/<int:group_id>/lessons/", views.LessonListView.as_view(), name="teacher-group-lessons"),
    path("teacher/lessons/", views.LessonListView.as_view(), name="teacher-lessons-all"),
    path("teacher/lesson/<int:lesson_id>/attendance/", views.AttendanceListView.as_view(), name="teacher-lesson-attendance"),

    # Маршруты для студента (Lab 3)
    path("student/profile/", views.ProfileView.as_view(), name="student-profile"),
    path("student/attendance/", views.MyAttendanceView.as_view(), name="student-attendance"),
]