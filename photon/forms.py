from django.contrib.auth.models import User
from django import forms

from .models import Profile, Snapshot


class LoginForm(forms.Form):
    username = forms.CharField(label="Пользователь",
                    widget=forms.TextInput(attrs={'placeholder': 'Пользователь'}))
    password = forms.CharField(label="Пароль",
                    widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="Пользователь")
    email = forms.EmailField(label="Почта")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def no_dublicate(self):
        """ проверка заполнения формы: * Пароли Совпадают * Пользователя с таким Nick'ом не существует"""
        valid = super(RegisterForm, self).is_valid()

        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_confirm']

        if pass1 != pass2:
            self.add_error("password_confirm", "Пароли не совпадают")
            """ WORKING: маленькая красная надпись между полями """
            return False
        elif User.objects.filter(username=username).exists() or Profile.objects.filter(nick=username).exists():
            self.add_error("username", "Данный username занят!")
            return False
        elif User.objects.filter(email=email).exists():
            self.add_error("email", "Пользователь с таким email уже зарегистрирован!")
            return False
        return valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'skill', 'gear']

    def nick_is_free(self):
        if User.objects.filter(username=self.nick).exists() or Profile.objects.filter(nick=self.nick).exists():
            self.add_error("nick", "Данный ник занят!")
            return False
        return True


class SnapshotForm(forms.ModelForm):
    class Meta:
        model = Snapshot
        exclude = ['author', 'timestamp', 'location', 'city', 'region', 'country']

