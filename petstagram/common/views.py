from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from petstagram.common.models import Like
from petstagram.photos.models import Photo
from petstagram.common.forms import CommentForm, SearchForm
from pyperclip import copy


# CBV for home page
class HomePage(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'photos'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains=pet_name,
            )

        return queryset


# FBV for home page
def home_page(request):
    photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        photos = photos.filter(
            tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
        )
    photos_per_page = 1
    paginator = Paginator(photos, photos_per_page)
    page = request.GET.get('page')

    photos = paginator.get_page(page)

    context = {
        "photos": photos,
        "comment_form": comment_form,
        "search_form": search_form,
    }

    return render(request, 'common/home-page.html', context=context)


@login_required
def like_functionality(request, photo_id):
    like_obj = Like.objects.filter(
        to_photo=photo_id
    ).first()

    if like_obj:
        like_obj.delete()
    else:
        like = Like(to_photo_id=photo_id, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


@login_required
def comment_functionality(request, photo_id: int):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')
