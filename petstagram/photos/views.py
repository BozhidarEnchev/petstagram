from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from petstagram.photos.models import Photo


class PhotoAddPage(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoAddForm
    template_name = 'photos/photo-add-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        # photo.save()
        # form.save_m2m()
        return super().form_valid(form)

# def photo_add_page(request):
#     form = PhotoAddForm(request.POST or None, request.FILES or None)
#
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('home')
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'photos/photo-add-page.html', context)


class PhotoEditPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    template_name = 'photos/photo-edit-page.html'
    form_class = PhotoEditForm

    def get_success_url(self):
        return reverse_lazy(
            'photo-details',
            kwargs={
                'pk': self.object.pk
            }
        )

    def test_func(self):
        profile = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return self.request.user == profile.user

# def photo_edit_page(request, pk: int):
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoEditForm(request.POST or None, instance=photo)
#
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('photo-details', pk)
#
#     context = {
#         'form': form,
#         'photo': photo,
#     }
#     return render(request, 'photos/photo-edit-page.html', context)


class PhotoDetailsPage(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['like'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()
        self.object.has_liked = self.object.like_set.filter(user=self.request.user).exists()

        return context


# def photo_details_page(request, pk: int):
#     photo = Photo.objects.get(pk=pk)
#     likes = photo.like_set.all()
#     comments = photo.comment_set.all()
#     comment_form = CommentForm()
#
#     context = {
#         "photo": photo,
#         "likes": likes,
#         "comments": comments,
#         "comment_form": comment_form,
#     }
#     return render(request, 'photos/photo-details-page.html', context=context)


@login_required
def photo_delete(request, pk: int):
    photo = Photo.objects.get(pk=pk)

    if request.user == photo.user:
        photo.delete()

    return redirect('home')
