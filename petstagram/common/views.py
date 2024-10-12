from django.shortcuts import render, redirect, resolve_url

from petstagram.common.models import Like
from petstagram.photos.models import Photo
from petstagram.common.forms import CommentForm
from pyperclip import copy


def home_page(request):
    photos = Photo.objects.all()
    comment_form = CommentForm()

    context = {
        "photos": photos,
        "comment_form": comment_form,
    }
    return render(request, 'common/home-page.html', context=context)


def like_functionality(request, photo_id):
    like_obj = Like.objects.filter(
        to_photo=photo_id
    ).first()

    if like_obj:
        like_obj.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def comment_functionality(request, photo_id: int):
    if request.POST :
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')
