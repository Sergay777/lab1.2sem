from django import forms
from .models import Attendance, Subject, Group, Teacher

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['id_lesson', 'id_student', 'status']

# ===== ФОРМЫ ДЛЯ ФИЛЬТРАЦИИ (Лаб 4) =====

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

class StudentFilterForm(forms.Form):
    last_name = forms.CharField(
        required=False,
        label="Фамилия студента",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

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