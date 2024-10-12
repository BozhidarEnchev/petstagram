from django.shortcuts import render, redirect, resolve_url

from petstagram.common.models import Like
from petstagram.photos.models import Photo
from pyperclip import copy


def home_page(request):
    photos = Photo.objects.all()

    context = {
        "photos": photos
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
