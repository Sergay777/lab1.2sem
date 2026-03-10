from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
import random
from users.models import User
from journal.models import (
    Period, Group, Subject, Student, Teacher,
    Type_lesson, Lesson, Att_Status, Attendance
)

FIRST_NAMES = ["Иван", "Пётр", "Сергей", "Алексей", "Дмитрий", "Егор", "Максим", "Михаил"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Фёдоров", "Егоров", "Максимов"]
MIDDLES = ["Иванович", "Петрович", "Сергеевич", "Алексеевич", "Дмитриевич", "Егорович", "Максимович", "Михайлович"]

SUBJECTS = ["Математика", "Информатика", "Физика"]
TYPE_LESSONS = [("lec", "Лекция"), ("lab", "Лабораторная"), ("sem", "Семинар")]
ATT_STATUSES = [
    ("Присутствовал", "Прис."),
    ("Отсутствовал", "Отс."),
    ("Болел", "Бол."),
    ("Уважительная причина", "Уваж."),
]

def _mk_username(base):
    """Делает уникальный username по базе."""
    base = base.lower().replace(" ", ".")
    candidate = base
    i = 1
    while User.objects.filter(username=candidate).exists():
        i += 1
        candidate = f"{base}.{i}"
    return candidate

@transaction.atomic
def create_demo_data(students_per_group=12, groups_count=2, lessons_per_group=6, seed=42):
    rnd = random.Random(seed)

    # 1) Базовый админ
    admin, created = User.objects.get_or_create(
        username="admin",
        defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"}
    )
    if created:
        admin.set_password("admin")
        admin.first_name = "Админ"
        admin.last_name = "Система"
        admin.save()

    # 2) Статусы посещаемости
    name2status = {}
    for name, short in ATT_STATUSES:
        st, _ = Att_Status.objects.get_or_create(name=name, defaults={"short_name": short})
        if st.short_name != short:
            st.short_name = short
            st.save(update_fields=["short_name"])
        name2status[name] = st
    default_status = name2status["Присутствовал"]

    # 3) Типы занятий
    id2type = {}
    for id_type, name in TYPE_LESSONS:
        t, _ = Type_lesson.objects.get_or_create(id_type=id_type, defaults={"name": name})
        if t.name != name:
            t.name = name
            t.save(update_fields=["name"])
        id2type[id_type] = t

    # 4) Предметы
    subjects = []
    for s in SUBJECTS:
        subj, _ = Subject.objects.get_or_create(name=s)
        subjects.append(subj)

    # 5) Периоды (две половины учебного года)
    today = date.today()
    year = today.year
    autumn_start = date(year, 9, 1)
    autumn_end = date(year, 12, 31)
    spring_start = date(year + 1, 2, 1)
    spring_end = date(year + 1, 6, 30)

    p_autumn, _ = Period.objects.get_or_create(
        name=f"{year}/{year+1} Осень",
        defaults={"date_start": autumn_start, "date_end": autumn_end, "term": "01"}
    )
    p_spring, _ = Period.objects.get_or_create(
        name=f"{year}/{year+1} Весна",
        defaults={"date_start": spring_start, "date_end": spring_end, "term": "02"}
    )
    periods = [p_autumn, p_spring]

    # 6) Преподаватели
    teachers = []
    for i in range(2):
        ln = LAST_NAMES[i]
        fn = FIRST_NAMES[i]
        mn = MIDDLES[i]
        uname = _mk_username(f"t.{ln}.{fn}")
        t_user, created = User.objects.get_or_create(
            username=uname,
            defaults={"first_name": fn, "last_name": ln, "email": f"{uname}@example.com", "is_staff": True}
        )
        if created:
            t_user.set_password("teacher")
            t_user.save()
        teacher, _ = Teacher.objects.get_or_create(
            user=t_user,
            defaults={
                "id_teacher": f"T{1000+i}",
                "last_name": ln,
                "first_name": fn,
                "second_name": mn,
                "academic_degree": "к.т.н.",
                "position": "преподаватель",
                "status": True
            }
        )
        teacher.subjects.set(subjects)
        teachers.append(teacher)

    # 7) Группы
    groups = []
    for i in range(groups_count):
        grp_code = f"ИКБО-0{i+1}-{str(year)[-2:]}"
        grp_name = f"Группа {i+1}"
        group, _ = Group.objects.get_or_create(
            id_group=grp_code,
            defaults={
                "name": grp_name,
                "year_priem": str(year),
                "study_form": "Очная",
                "level": "Бакалавриат",
                "faculty": "ИТ",
                "department": "Кафедра ИС",
                "term_number": "01",
                "number_of_active_students": str(students_per_group),
                "status": True,
                "semestr": "Осень",
            }
        )
        groups.append(group)

    # 8) Студенты
    students_by_group = {g: [] for g in groups}
    student_counter = 0
    for g in groups:
        for _ in range(students_per_group):
            ln = rnd.choice(LAST_NAMES)
            fn = rnd.choice(FIRST_NAMES)
            mn = rnd.choice(MIDDLES)
            uname = _mk_username(f"s.{ln}.{fn}")
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={"first_name": fn, "last_name": ln, "email": f"{uname}@example.com"}
            )
            if created:
                u.set_password("student")
                u.save()
            student, _ = Student.objects.get_or_create(
                user=u,
                defaults={
                    "student_id": f"S{10000+student_counter}",
                    "id_record_book": f"RB{20000+student_counter}",
                    "id_group": g,
                    "last_name": ln,
                    "first_name": fn,
                    "second_name": mn,
                    "starosta": False,
                    "expelled": False,
                    "status": "обучается",
                }
            )
            students_by_group[g].append(student)
            student_counter += 1

    # 9) Занятия
    all_lessons = []
    for g in groups:
        for per in periods:
            start = per.date_start or today
            end = per.date_end or (start + timedelta(days=60))
            if start > end:
                start, end = end, start
            days_span = max((end - start).days, 14)
            for i in range(lessons_per_group):
                dt = start + timedelta(days=rnd.randint(0, days_span))
                subj = rnd.choice(subjects)
                teacher = rnd.choice(teachers)
                ttype = rnd.choice(list(id2type.values()))
                lesson, created = Lesson.objects.get_or_create(
                    id_lesson=f"L{g.id_group}-{per.term}-{i+1}",
                    id_group=g,
                    id_subject=subj,
                    id_teacher=teacher,
                    period=per,
                    defaults={
                        "type": ttype,
                        "topic": f"{subj.name}: тема {i+1}",
                        "date": dt,
                        "status": True,
                        "changed_by": teacher.user,
                    }
                )
                if not created:
                    updates = False
                    if lesson.type_id != ttype.id:
                        lesson.type = ttype
                        updates = True
                    if lesson.date != dt:
                        lesson.date = dt
                        updates = True
                    if lesson.topic != f"{subj.name}: тема {i+1}":
                        lesson.topic = f"{subj.name}: тема {i+1}"
                        updates = True
                    if updates:
                        lesson._history_user = teacher.user
                        lesson.save()
                all_lessons.append((lesson, teacher))

    # 10) Посещаемость
    for lesson, teacher in all_lessons:
        group_students = students_by_group[lesson.id_group]
        for st in group_students:
            status = default_status if rnd.random() < 0.8 else rnd.choice(list(name2status.values()))
            att, created = Attendance.objects.get_or_create(
                id_lesson=lesson,
                id_student=st,
                defaults={
                    "status": status,
                    "changed_by": teacher.user,
                }
            )
            if not created and att.status_id != status.id:
                att.status = status
                att._history_user = teacher.user
                att.save(update_fields=["status"])

    return {
        "periods": Period.objects.count(),
        "groups": Group.objects.count(),
        "subjects": Subject.objects.count(),
        "teachers": Teacher.objects.count(),
        "students": Student.objects.count(),
        "lessons": Lesson.objects.count(),
        "attendance": Attendance.objects.count(),
        "att_statuses": Att_Status.objects.count(),
        "type_lessons": Type_lesson.objects.count(),
    }

class Command(BaseCommand):
    help = "Создаёт тестовые данные (периоды, группы, предметы, преподаватели, студенты, занятия, посещаемость)."

    def add_arguments(self, parser):
        parser.add_argument("--students-per-group", type=int, default=12, help="Сколько студентов в каждой группе")
        parser.add_argument("--groups", type=int, default=2, help="Сколько групп создать")
        parser.add_argument("--lessons-per-group", type=int, default=6, help="Сколько занятий на группу в каждом периоде")
        parser.add_argument("--seed", type=int, default=42, help="Seed для детерминированности")

    def handle(self, *args, **options):
        stats = create_demo_data(
            students_per_group=options["students_per_group"],
            groups_count=options["groups"],
            lessons_per_group=options["lessons_per_group"],
            seed=options["seed"],
        )
        self.stdout.write(self.style.SUCCESS("Готово! Создано/обновлено:"))
        for k, v in stats.items():
            self.stdout.write(f"  {k}: {v}")