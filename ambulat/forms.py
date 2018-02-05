# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.db import transaction
from django.core import validators
from .models import *
import re
from mysite.models import get_object_or_none


def RaiseIfNotRulePassword(pwd):
    if len(pwd) < 8 or (re.search(r'[A-Z]+', pwd) or re.search(r'[А-Я]+', pwd)) is None \
            or (re.search(r'[a-z]+', pwd) or re.search(r'[а-я]+', pwd)) is None \
            or re.search(r'[0-9]+', pwd) is None:
            raise forms.ValidationError('Мінімум 8 символів (обов’язкові: хоча б одна цифра, '
                                        'буква верхнього регістру, буква нижнього регістру)')


def get_years():
    cur_year = datetime.date.today().year
    return [i for i in range(cur_year, cur_year-60, -1)]


class UserFullForm(UserCreationForm):
    username = forms.CharField(label=u"Ім'я користувача", min_length=3, max_length=30,
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      "Обов'язкове поле. 30 або менше символів. "
                                      "Тільки букви, цифри, а також символи: @/./+/-/_", 'invalid'),
        ],
        widget=forms.TextInput)
    last_name = forms.CharField(label=u"Прізвище", min_length=3, max_length=30,
                                # help_text=u'Введіть від 3 до 30 символів.',
                                widget=forms.TextInput)
    first_name = forms.CharField(label=u"Им'я", min_length=3, max_length=30, widget=forms.TextInput)
    middlename = forms.CharField(label=u"По батькові", min_length=3, max_length=30, widget=forms.TextInput)
    birthday = forms.DateField(label=u"День народження", widget=SelectDateWidget(years=get_years()))
    email = forms.EmailField(label=u"Email", max_length=254)

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "middlename", "birthday", "email")

    def clean_birthday(self):
        try:
            last_name = self.cleaned_data["last_name"]
            first_name = self.cleaned_data["first_name"]
            middlename = self.cleaned_data["middlename"]
            birthday = self.cleaned_data["birthday"]
            up_id = get_user_profile_id(last_name, first_name, middlename, 
                                        birthday.strftime('%Y-%m-%d'))
        except KeyError:
            up_id = 0

        if up_id > 0:
            raise forms.ValidationError('Користувач з таким ПІБ та датою народження вже існує.')

    def clean_password1(self):
        pwd = self.cleaned_data.get("password1")
        RaiseIfNotRulePassword(pwd)
        return pwd


@transaction.atomic
def save_patient(request, birthdaydt):
    p, created = Patient.objects.get_or_create(lastname=request.POST['last_name'],
                                               firstname=request.POST['first_name'],
                                               middlename=request.POST['middlename'],
                                               birthday=birthdaydt)
    Patient.objects.filter(id=p.id).update(cardno=str(100000+p.id))
    return p.id


class RegisterFormView(FormView):
    form_class = UserFullForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    success_url = "/ambulat/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "ambulat/register.html"

    def get_birthday(self):
        return datetime.datetime.strptime('%s.%s.%s' % (self.request.POST['birthday_day'],
                                                        self.request.POST['birthday_month'],
                                                        self.request.POST['birthday_year']), '%d.%m.%Y')

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        user = form.save()
        birthday_dt = self.get_birthday()
        patient_id = save_patient(self.request, birthday_dt)
        up = UserProfile(user_id=user.id,
                         middlename=self.request.POST['middlename'],
                         birthday=birthday_dt,
                         patientid=patient_id)
        up.save()
        default_group = get_object_or_none(Group, name=u'Пацієнт')
        if default_group:
            default_group.user_set.add(user)
        password = self.request.POST['password2']
        self.request.user = authenticate(username=user.username, password=password)
        if self.request.user is not None:
            login(self.request, self.request.user)

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
