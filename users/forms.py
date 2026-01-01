from django import forms
from django.contrib.auth.models import User
class RegisterForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
 
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин уже занят. Выберите другой.")
        return username
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data