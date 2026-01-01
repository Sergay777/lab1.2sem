from django.contrib.auth.mixins import UserPassesTestMixin

class TeacherRequiredMixin(UserPassesTestMixin):
    """Миксин, допускающий только пользователей с профилем преподавателя."""
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return hasattr(user, 'teacher') and user.teacher is not None

class StudentRequiredMixin(UserPassesTestMixin):
    """Миксин, допускающий только пользователей с профилем студента."""
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return hasattr(user, 'student') and user.student is not None