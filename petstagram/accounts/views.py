from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import AppUserCreationForm, ProfileEditForm
from petstagram.accounts.models.app_profile import Profile

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(request=self.request, user=self.object)

        return response


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to perform this action.")


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user.profile

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to perform this action.")


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        photos_with_likes = self.object.photo_set.annotate(likes_count=Count('like'))
        context['total_likes_count'] = sum(p.likes_count for p in photos_with_likes)
        context['total_pets_count'] = self.object.pet_set.count()
        context['total_photos_count'] = self.object.photo_set.count()

        return context

