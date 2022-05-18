from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django_eolimp.settings import SECRET_KEY_TEACHER
from testing.models import Student, Teacher, Group, Solution, Lecture, Problem

from testing.widget import BootstrapDateTimePickerInput


User = get_user_model()


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
                               max_length=32, label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Код доступу'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields + ('secret_key', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user

    def clean(self):
        super().clean()
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key:
            if secret_key != SECRET_KEY_TEACHER:
                raise forms.ValidationError(
                    'You must be a teacher to sign up as a teacher!',
                    code='password_mismatch',
                )


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
                                max_length=32, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Група")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields + ('group', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._student = True
        user.save()
        student = Student.objects.create(user=user, group=self.cleaned_data['group'])
        return user


class CreateSolutionForm(forms.ModelForm):
    solution_code = forms.CharField(widget=forms.Textarea(), label='')

    class Meta:
        model = Solution
        fields = ['solution_code']



class CreateProblemForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    title = forms.CharField(max_length=255)
    description = forms.Textarea()
    problem_value = forms.FloatField()
    deadline = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )
    input_data = forms.FileField()
    output_data = forms.FileField()

    class Meta:
        model = Problem
        fields = ['groups', 'title', 'description', 'problem_value', 'deadline', 'input_data', 'output_data']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CreateProblemForm, self).save(**kwargs)
        instance.teacher_id = Teacher.objects.get(user=user)
        instance.save()
        return instance


class LectureCreateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    title = forms.CharField(max_length=255)
    description = forms.Textarea()

    class Meta:
        model = Lecture
        fields = ['groups', 'title', 'description']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(LectureCreateForm, self).save(**kwargs)
        instance.teacher_id = Teacher.objects.get(user=user)
        instance.save()
        return instance

