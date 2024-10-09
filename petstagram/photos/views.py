from django.shortcuts import render

from petstagram.photos.models import Photo


def photo_add_page(request):
    return render(request, 'photos/photo-add-page.html')


def photo_edit_page(request, pk: int):
    return render(request, 'photos/photo-edit-page.html')


def photo_details_page(request, pk: int):
    photos = Photo.objects.filter(pk=pk)
    context = {
        "photos": photos
    }
    return render(request, 'photos/photo-details-page.html', context=context)
