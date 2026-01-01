from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import AttendanceForm
from .filters import (  # <-- ДОБАВЛЕНО: импорт форм фильтрации
    LessonFilterForm,
    StudentFilterForm,
    AttendanceListFilterForm,
    StudentAttendanceFilterForm
)
from django.db.models import Count, Q
from .models import Student, Group, Attendance, Lesson, Subject, Teacher, Period, Type_lesson, Att_Status

# ===== Импорты для CBV =====
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from django.shortcuts import get_object_or_404
from .mixins import TeacherRequiredMixin, StudentRequiredMixin

# ===== ФУНКЦИОНАЛЬНЫЕ ПРЕДСТАВЛЕНИЯ (старые) =====

def index(request):
    context = {
        'welcome': "Добро пожаловать, уважаемый пользователь!",
        'menu': []
    }
    return render(request, 'journal/index.html', context)

def about(request):
    return render(request, 'journal/about.html', {})

def contacts(request):
    return render(request, 'journal/contacts.html', {})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_add')
    else:
        form = AttendanceForm()
    return render(request, 'journal/add_attendance.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_teacher:
        return redirect('home')
    student = getattr(request.user, 'student', None)
    return render(request, 'journal/profile.html', {'student': student})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_panel(request):
    return render(request, 'journal/teacher_panel.html')

@login_required
def attendance_list(request):
    return render(request, 'journal/attendance_list.html', {})

@login_required
def attendance_stats(request):
    stats = Student.objects.annotate(
        total=Count('attendance'),
        absences=Count('attendance', filter=Q(attendance__present=False))
    )
    for student in stats:
        if student.total > 0:
            student.attendance_percent = round(((student.total - student.absences) / student.total) * 100, 1)
        else:
            student.attendance_percent = 0
    return render(request, 'journal/stats.html', {'stats': stats})

@login_required
def my_attendance(request):
    if not request.user.is_student:
        return redirect('home')
    student = getattr(request.user, 'student', None)
    if not student:
        return render(request, 'journal/my_attendance.html', {'attendance_list': []})
    attendance_list = student.attendance_set.all().order_by('-date')
    return render(request, 'journal/my_attendance.html', {'attendance_list': attendance_list})

@login_required
def group_stats(request):
    stats = Group.objects.annotate(
        student_count=Count('student', distinct=True),
        present_count=Count('student__attendance', filter=Q(student__attendance__present=True))
    )
    return render(request, 'journal/group_stats.html', {'stats': stats})

# ===== КЛАССЫ-ПРЕДСТАВЛЕНИЯ ДЛЯ ПРЕПОДАВАТЕЛЯ (Lab 3) =====

class GroupListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Group
    template_name = "teacher/groups.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        queryset = Group.objects.all().order_by("name")
        
        # Создаем форму фильтрации (для Group можно добавить фильтры при необходимости)
        # В текущей реализации фильтрация для групп не требуется, но оставляем структуру
        self.filter_form = StudentFilterForm(self.request.GET)  # Можно использовать StudentFilterForm для поиска по группам
        
        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data
            # Если нужны фильтры для групп, добавьте их здесь
            # Например, фильтр по названию группы:
            # if cd.get('name'):
            #     queryset = queryset.filter(name__icontains=cd['name'])
            pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список учебных групп"
        context["filter_form"] = getattr(self, 'filter_form', StudentFilterForm())
        
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context["filter_params"] = query_params.urlencode()
        
        return context

class StudentListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Student
    template_name = "teacher/group_students.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        self.group = get_object_or_404(Group, pk=group_id)
        
        queryset = Student.objects.filter(id_group=self.group).select_related("user").order_by("last_name", "first_name")
        
        # Применяем фильтрацию
        self.filter_form = StudentFilterForm(self.request.GET)
        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data
            if cd.get('last_name'):
                queryset = queryset.filter(last_name__icontains=cd['last_name'])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["title"] = f"Студенты группы {self.group.name}"
        context["filter_form"] = getattr(self, 'filter_form', StudentFilterForm())
        
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context["filter_params"] = query_params.urlencode()
        
        return context

class LessonListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Lesson
    template_name = "teacher/lessons.html"
    context_object_name = "lessons"
    paginate_by = 10

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        
        # Базовый QuerySet в зависимости от контекста
        if group_id:
            self.group = get_object_or_404(Group, pk=group_id)
            queryset = Lesson.objects.filter(id_group=self.group)
        else:
            # Если группа не указана, показываем все занятия преподавателя
            queryset = Lesson.objects.filter(id_teacher=self.request.user.teacher)
        
        # Применяем фильтрацию
        self.filter_form = LessonFilterForm(self.request.GET)
        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data
            if cd.get('date'):
                queryset = queryset.filter(date=cd['date'])
            if cd.get('subject'):
                queryset = queryset.filter(id_subject=cd['subject'])
            if cd.get('group'):
                queryset = queryset.filter(id_group=cd['group'])
        
        return queryset.select_related("id_subject", "id_teacher", "type", "period").order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = getattr(self, "group", None)
        if group:
            context["group"] = group
            context["title"] = f"Занятия группы {group.name}"
        else:
            context["title"] = "Мои занятия"
        
        context["filter_form"] = getattr(self, 'filter_form', LessonFilterForm())
        
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context["filter_params"] = query_params.urlencode()
        
        return context

class AttendanceListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Attendance
    template_name = "teacher/lesson_attendance.html"
    context_object_name = "attendances"
    paginate_by = 30

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_id")
        self.lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        queryset = Attendance.objects.filter(id_lesson=self.lesson)
        
        # Применяем фильтрацию
        self.filter_form = AttendanceListFilterForm(self.request.GET)
        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data
            
            # Фильтр по статусу
            if cd.get('status') and cd['status']:
                if cd['status'] == 'present':
                    # Ищем статусы, содержащие "Присут"
                    queryset = queryset.filter(status__name__icontains='Присут')
                elif cd['status'] == 'absent':
                    # Ищем статусы, содержащие "Отсут" или "Бол" или "Уваж"
                    queryset = queryset.filter(
                        Q(status__name__icontains='Отсут') |
                        Q(status__name__icontains='Бол') |
                        Q(status__name__icontains='Уваж')
                    )
            
            # Фильтр по фамилии
            if cd.get('last_name'):
                queryset = queryset.filter(id_student__last_name__icontains=cd['last_name'])
        
        return queryset.select_related("id_student__user", "status").order_by("id_student__last_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = self.lesson
        context["group"] = self.lesson.id_group
        context["title"] = f"Посещаемость: {self.lesson.id_subject.name}, {self.lesson.date}"
        context["filter_form"] = getattr(self, 'filter_form', AttendanceListFilterForm())
        
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context["filter_params"] = query_params.urlencode()
        
        return context

# ===== КЛАССЫ-ПРЕДСТАВЛЕНИЯ ДЛЯ СТУДЕНТА (Lab 3) =====

class ProfileView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "student/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context["student"] = student
        context["title"] = "Мой профиль"
        return context

class MyAttendanceView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = Attendance
    template_name = "student/my_attendance.html"
    context_object_name = "attendances"
    paginate_by = 15

    def get_queryset(self):
        student = self.request.user.student
        queryset = Attendance.objects.filter(id_student=student)
        
        # Применяем фильтрацию
        self.filter_form = StudentAttendanceFilterForm(self.request.GET)
        if self.filter_form.is_valid():
            cd = self.filter_form.cleaned_data
            if cd.get('date'):
                queryset = queryset.filter(id_lesson__date=cd['date'])
            if cd.get('subject'):
                queryset = queryset.filter(id_lesson__id_subject=cd['subject'])
            if cd.get('teacher'):
                queryset = queryset.filter(id_lesson__id_teacher=cd['teacher'])
            if cd.get('status') and cd['status']:
                # Фильтр по статусу посещения
                if cd['status'] == 'present':
                    queryset = queryset.filter(status__name__icontains='Присут')
                elif cd['status'] == 'absent':
                    queryset = queryset.filter(
                        Q(status__name__icontains='Отсут') |
                        Q(status__name__icontains='Бол') |
                        Q(status__name__icontains='Уваж')
                    )
        
        return queryset.select_related("id_lesson__id_subject", "id_lesson__id_teacher__user", "status").order_by("-id_lesson__date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Моя посещаемость"
        context["filter_form"] = getattr(self, 'filter_form', StudentAttendanceFilterForm())
        
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context["filter_params"] = query_params.urlencode()
        
        return context