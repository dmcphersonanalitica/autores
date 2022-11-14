from django.contrib.auth.models import Permission
from django.forms import *
from django import forms
from Login.models import User
from MECS_Autores.models import Autores


class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].label = 'Email'
        self.fields['username'].label = 'Usuario'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                at = Autores.objects.filter(user_id=u.id)
                if len(at) > 0:
                    a = Autores.objects.get(user_id=u.id)
                    a.correo = self.cleaned_data['email']
                    a.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_active', 'is_superuser']
        widgets = {
            'email': EmailInput(
                attrs={
                    'placeholder': 'Email',
                }
            ),
            'is_active': CheckboxInput(
                attrs={
                    'class': 'custom-control-input'
                }
            ),
            'is_superuser': CheckboxInput(
                attrs={
                    'class': 'custom-control-input'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Usuario',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Contraseña',
                }
            ),
        }
        exclude = ['last_login', 'date_joined', 'is_staff']


class UserProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Email'
        self.fields['username'].label = 'Usuario'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                u.save()
                at = Autores.objects.filter(user_id=u.id)
                if len(at) > 0:
                    a = Autores.objects.get(user_id=u.id)
                    a.correo = self.cleaned_data['email']
                    a.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su usuario',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups', 'password']

