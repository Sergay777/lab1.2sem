from django.contrib import admin
from .models import (
    Period, Group, Subject, Student, Teacher,
    Type_lesson, Lesson, Att_Status, Attendance
)

# Inline для студентов
class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

# Inline для посещаемости
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'term')
    search_fields = ('name',)
    list_filter = ('term',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id_group', 'name', 'year_priem', 'study_form', 'faculty')
    search_fields = ('id_group', 'name', 'faculty')
    list_filter = ('study_form', 'faculty')
    inlines = [StudentInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'second_name', 'id_group', 'status')
    search_fields = ('last_name', 'first_name', 'student_id')
    list_filter = ('id_group', 'status')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'second_name', 'position')
    search_fields = ('last_name', 'first_name', 'id_teacher')
    list_filter = ('position',)

@admin.register(Type_lesson)
class Type_lessonAdmin(admin.ModelAdmin):
    list_display = ('id_type', 'name')
    search_fields = ('name',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id_lesson', 'id_subject', 'id_group', 'date', 'type', 'id_teacher')
    search_fields = ('id_lesson', 'topic')
    list_filter = ('id_group', 'id_subject', 'date', 'type')
    inlines = [AttendanceInline]

@admin.register(Att_Status)
class Att_StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id_lesson', 'id_student', 'status', 'time_create')
    search_fields = ('id_student__last_name', 'id_lesson__id_lesson')
    list_filter = ('status', 'id_lesson__id_group')