from django import forms
from .models import Subject, Group, Teacher, Att_Status

# Форма фильтрации списка занятий преподавателя
class LessonFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Дата занятия",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    subject = forms.ModelChoiceField(
        required=False,
        label="Предмет",
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    group = forms.ModelChoiceField(
        required=False,
        label="Группа",
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

# Форма фильтрации списка студентов (например, список студентов группы)
class StudentFilterForm(forms.Form):
    last_name = forms.CharField(
        required=False,
        label="Фамилия студента",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

# Форма фильтрации списка посещаемости занятия
class AttendanceListFilterForm(forms.Form):
    status_choices = [
        ("", "любой"),
        ("present", "Присутствовал"),
        ("absent", "Отсутствовал"),
    ]
    status = forms.ChoiceField(
        required=False,
        label="Статус посещения",
        choices=status_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False,
        label="Фамилия студента",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

# Форма фильтрации списка посещаемости студента
class StudentAttendanceFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Дата занятия",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    subject = forms.ModelChoiceField(
        required=False,
        label="Предмет",
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    teacher = forms.ModelChoiceField(
        required=False,
        label="Преподаватель",
        queryset=Teacher.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус посещения",
        choices=AttendanceListFilterForm.status_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )