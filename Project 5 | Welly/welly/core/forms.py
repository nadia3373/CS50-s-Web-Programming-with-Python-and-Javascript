from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import *


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_start_time"]

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["appointment_start_time"].choices = choices


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["country", "city", "street", "building", "office", "domain", "name", "logo", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "country": self.fields[field].widget.attrs.update({'class': 'form-control'})
            else: self.fields[field].widget.attrs.update({'class': 'form-control form-select'})


class CompanyEditForm(ModelForm):
    class Meta:
        model = Company
        fields = ["country", "city", "street", "building", "office", "name", "logo", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "country": self.fields[field].widget.attrs.update({'class': 'form-control'})
            else: self.fields[field].widget.attrs.update({'class': 'form-control form-select'})


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: self.fields[field].widget.attrs.update({'class': 'form-control'})


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ["name", "length", "price", "description", "image", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "status": self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserForm(UserCreationForm):
    dob = forms.DateField(label='Date of birth', widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autofocus': 'true'}))
    email=forms.EmailField(label='Email address', max_length=64, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1=forms.CharField(label="Create a password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2=forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number=forms.CharField(validators=[RegexValidator(regex='^[0-9]{10}$', message='Phone number must contain 10 digits')], max_length=10, min_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = tuple(x for x in UserCreationForm.Meta.fields if x != 'username') + ('dob', 'email', 'first_name', 'last_name', 'phone_number', 'photo')


class UserEditForm(UserForm):
    dob = forms.DateField(label='Date of birth', widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    email=forms.EmailField(label='Email address', max_length=64, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1=forms.CharField(label="Create a password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2=forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number=forms.CharField(validators=[RegexValidator(regex='^[0-9]{10}$', message='Phone number must contain 10 digits')], max_length=10, min_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta(UserCreationForm.Meta):
        fields = tuple(x for x in UserForm.Meta.fields if x != 'username') + ('dob', 'email', 'first_name', 'last_name', 'phone_number', 'photo')


class WHForm(ModelForm):
    workday_start = forms.TimeField(widget=forms.TimeInput(format='%H'))
    workday_finish = forms.TimeField(widget=forms.TimeInput(format='%H'))
    class Meta:
        model = Working_hours
        fields = ['workday_start', 'workday_finish']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: self.fields[field].widget.attrs.update({'class': 'form-control'})