from django.shortcuts import render
from petstagram.photos.models import Photo


def home_page(request):
    photos = Photo.objects.all()

    context = {
        "photos": photos
    }
    return render(request, 'common/home-page.html', context=context)


def like_functionality(request, pk):
    pass


def copy_link_to_clipboard(request, pk):
    pass
