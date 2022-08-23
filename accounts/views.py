from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, login, get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm
from accounts.models import Profile


class LoginView(LoginView):
    template_name = "registration/login.html"
    post_redirect = None


    def get(self, request, *args, **kwargs):
        self.object = None
        post_redirect = request.META.get('HTTP_REFERER')
        print(self.object,post_redirect)
        return super().get(request, *args, **kwargs)
#
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.post_redirect)
#
#
#     def post(self, request, *args, **kwargs):
#         """Logout may be done via POST."""
#         self.object, self.redirect_url = self.get( request, *args, **kwargs)
#         print(self.redirect_url)
#         return self.object, self.redirect_url
#     #
#     #
#     # def get_redirect_url(self):
#     #     """Return the user-originating redirect URL if it's safe."""
#     #     x,redirect_url = self.post()
#     #     print(self.request)
#     #     redirect_to = redirect_url
#     #     print(redirect_to)
#     #     url_is_safe = url_has_allowed_host_and_scheme(
#     #         url=redirect_to,
#     #         allowed_hosts=self.get_success_url_allowed_hosts(),
#     #         require_https=self.request.is_secure(),
#     #     )
#     #     return HttpResponseRedirect(self.request.META.get('HTTP_REFERER')) if url_is_safe else ""
#     if post:
#         def get_success_url(self):
#             x, redirect_url = self.post()
#             print(self.request)
#             redirect_to = redirect_url
#             print(self.request.META.get('HTTP_REFERER','/'))
#             return HttpResponseRedirect(redirect_to)
#

def register_view(request, *args, **kwargs):

    if request.method == 'POST':
        try:
            form = MyUserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('webapp:IndexView')
        except: ValidationError
    else:
        form = MyUserCreationForm()
    return render(request, 'user_create.html', context={'form': form})

class UsersView(PermissionRequiredMixin, ListView):
    template_name = 'usersall.html'
    model = get_user_model()
    context_object_name = 'users'
    permission_required = 'webapp.view_user'

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        return self.request.user.groups.filter(name__in=('Project Manager','Team Lead',)).exists()


class UserDetailView(DetailView):
    template_name = 'user.html'
    model = get_user_model()
    context_object_name = 'user'
    # permission_required = 'accounts.view_user'




class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'


    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)


    def form_valid(self, form, profile_form):
        if self.request.user:
            response = super().form_valid(form)
            profile_form.save()
            return response
        else:
            HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)


    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)


    def get_success_url(self):
        return reverse('accounts:UserDetailView', kwargs={'pk': self.object.pk})

class UserPasswordChangeView(PasswordChangeView):

    template_name = 'registration/password_change_form.html'

    def get_success_url(self):
        return reverse('accounts:UserDetailView', kwargs={'pk': self.request.user.pk})