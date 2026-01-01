from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
# FIXED: Добавлен правильный импорт модели пользователя
from django.contrib.auth import get_user_model

User = get_user_model()  # FIXED: Объявление переменной User

class Period(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Период')
    date_start = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    date_end = models.DateField(verbose_name='Дата конца', blank=True, null=True)
    term = models.CharField(max_length=2, verbose_name='Срок')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
        ordering = ['-date_start']

    def __str__(self):
        return self.name

class Group(models.Model):
    id_group = models.CharField(max_length=100, unique=True, verbose_name='Номер группы')
    name = models.CharField(max_length=200, verbose_name='Группа')
    year_priem = models.CharField(max_length=200, verbose_name='Год приема')
    study_form = models.CharField(max_length=200, blank=True, null=True, verbose_name='Форма обучения')
    level = models.CharField(max_length=200, blank=True, null=True, verbose_name='Уровень')
    faculty = models.CharField(max_length=200, blank=True, null=True, verbose_name='Факультет')
    department = models.CharField(max_length=200, blank=True, null=True, verbose_name='Подразделение')
    term_number = models.CharField(max_length=2, blank=True, verbose_name='Период')
    number_of_active_students = models.CharField(max_length=2, blank=True, verbose_name='Количество студентов')
    status = models.BooleanField(default=False, blank=True)
    semestr = models.CharField(max_length=10, blank=True, verbose_name='Семестр')
    history = HistoricalRecords()

    class Meta:
        unique_together = [("id_group", "name")]
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name

class Student(models.Model):
    # FIXED: Оставлено settings.AUTH_USER_MODEL, это корректно для OneToOneField
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Пользователь')
    student_id = models.CharField(max_length=200, blank=True, verbose_name='Student_ID')
    id_record_book = models.CharField(max_length=200, blank=True, null=True)
    id_group = models.ForeignKey('Group', on_delete=models.PROTECT, verbose_name='Номер группы', blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    second_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Отчество')
    starosta = models.BooleanField(default=False, blank=True)
    expelled = models.BooleanField(default=False, blank=True)
    status = models.CharField(max_length=200, verbose_name='Статус', blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name', 'second_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name or ''}".strip()

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.second_name}"

class Teacher(models.Model):
    # FIXED: Оставлено settings.AUTH_USER_MODEL, это корректно для OneToOneField
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Пользователь')
    id_teacher = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    second_name = models.CharField(max_length=200, verbose_name='Отчество')
    subjects = models.ManyToManyField(Subject, verbose_name='Предметы', blank=True)
    academic_degree = models.CharField(max_length=200, verbose_name='Степень', blank=True)
    position = models.CharField(max_length=200, verbose_name='Должность', blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name or ''}".strip()

class Type_lesson(models.Model):
    id_type = models.CharField(max_length=100, unique=True, verbose_name='ID')
    name = models.CharField(max_length=200, unique=True, verbose_name='Тип занятия')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Тип занятия'
        verbose_name_plural = 'Типы занятий'

    def __str__(self):
        return self.name

class Lesson(models.Model):
    id_lesson = models.CharField(max_length=100, verbose_name='Номер занятия в расписании')
    id_group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Номер группы')
    id_subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name='Предмет')
    id_teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='ID учителя')
    type = models.ForeignKey(Type_lesson, on_delete=models.PROTECT, blank=True, verbose_name='Тип занятия')
    topic = models.CharField(max_length=200, blank=True, verbose_name='Тема занятия')
    date = models.DateField()
    status = models.BooleanField(default=False)
    period = models.ForeignKey(Period, on_delete=models.PROTECT, verbose_name='Период')
    time_create = models.DateField(auto_now_add=True, blank=True, verbose_name='Время создания')
    time_update = models.DateField(auto_now=True, blank=True, verbose_name='Время обновления')
    # FIXED: Заменено на объявленную переменную User
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Создал')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['-date']

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.id_subject.name + ' - ' + self.id_group.name

class Att_Status(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True)
    short_name = models.CharField(max_length=200, verbose_name='Короткое название')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['id']

    def __str__(self):
        return self.name

class Attendance(models.Model):
    id_lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='Номер занятия')
    id_student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name='Номер студента')
    time_create = models.DateField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateField(auto_now=True, verbose_name='Время обновления')
    status = models.ForeignKey(Att_Status, on_delete=models.SET_DEFAULT, default=1, verbose_name='Статус')
    # FIXED: Заменено на объявленную переменную User для единообразия
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='Создал')
    history = HistoricalRecords()

    class Meta:
        unique_together = [("id_lesson", "id_student")]
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.id_student.last_name + ' ' + self.id_student.first_name + ' ' + self.id_student.second_name