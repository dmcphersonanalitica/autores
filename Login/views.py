import requests
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.conf import settings
from Login.forms import UserForm, UserProfileForm
from Login.mixins import IsSuperuserMixin
from Login.models import User
from core.settings import STATIC_URL


class LoginFormView(LoginView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Iniciar sesión"
        return context


class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, IsSuperuserMixin, ListView):
    model = User
    template_name = 'user/list.html'
    url_redirect = reverse_lazy('mecs:dashboard')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                position = 1
                for i in User.objects.all().select_related('autores'):
                    item = i.toJson()
                    if hasattr(i, 'autores'):
                        if i.autores is not None:
                            item['full_name'] = i.autores.__str__()
                    else:
                        item['full_name'] = i.get_full_name()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = '¡Ha ocurrido un error!'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios'
        context['createUrl'] = reverse_lazy('login:user_add')
        context['action'] = 'list'
        context['father'] = 'usuario'
        return context


class UserCreateView(LoginRequiredMixin, IsSuperuserMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login:user_list')
    url_redirect = reverse_lazy('login:user_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna operación'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear usuario'
        context['listUrl'] = reverse_lazy('login:user_list')
        context['action'] = 'add'
        context['father'] = 'usuario'
        return context


class UserUpdateView(LoginRequiredMixin, IsSuperuserMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login:user_list')
    url_redirect = reverse_lazy('login:user_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            if self.object.is_superuser and not request.user.is_superuser:
                data['error'] = 'No tiene permiso para editar este usuario.'
            else:
                action = request.POST['action']
                if action == 'edit':
                    form = self.get_form()
                    data = form.save()
                else:
                    data['error'] = 'No ha ingresado a ninguna operación'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['listUrl'] = reverse_lazy('login:user_list')
        context['action'] = 'edit'
        context['father'] = 'usuario'
        return context


class UserDeleteView(LoginRequiredMixin, IsSuperuserMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('login:user_list')
    url_redirect = reverse_lazy('login:user_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def generate_request(self, url, params={}):
        try:
            response = requests.get(url, verify=False)

            if response.status_code == 200:
                return response.json()
        except Exception as ex:
            pass

    def get_author_image(self, params={}):
        lowerNames = self.object.autores.nombre.lower().replace(' ', '-', 1)
        lowerLastNames = self.object.autores.apellidos.lower().replace(' ', '-', 1)
        lowerFullNames = lowerNames + '-' + lowerLastNames
        email = self.object.autores.correo

        response = self.generate_request('https://dmcphersoneditorial.com:3001/api/autor/by-full-name/' +
                                         lowerFullNames, params)
        if response:
            imageUrl = response.get('picture_address')
            return imageUrl

        response = self.generate_request('https://dmcphersoneditorial.com:3001/api/autor/by-email/' + email, params)
        if response:
            imageUrl = response.get('picture_address')
            return imageUrl

        return '{}{}'.format(STATIC_URL, 'image/Author.jpg')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar usuario'
        context['listUrl'] = reverse_lazy('login:user_list')
        if hasattr(self.object, 'autores'):
            if self.object is not None:
                context['imageUrl'] = self.get_author_image()
        else:
            context['imageUrl'] = '{}{}'.format(STATIC_URL, 'image/Author.jpg')
        context['action'] = 'delete'
        context['father'] = 'usuario'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('mecs:dashboard')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar perfil'
        context['entity'] = 'Perfil'
        context['listUrl'] = reverse_lazy('mecs:dashboard')
        context['action'] = 'edit'
        context['father'] = 'usuario'
        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['old_password'].label = 'Contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password1'].label = 'Nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su nueva contraseña'
        form.fields['new_password2'].label = 'Confirmar nueva contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar contraseña'
        context['entity'] = 'Password'
        context['listUrl'] = reverse_lazy('mecs:dashboard')
        context['action'] = 'edit'
        context['father'] = 'usuario'
        return context
