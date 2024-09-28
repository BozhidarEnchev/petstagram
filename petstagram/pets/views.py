from django.shortcuts import render


def pet_add(request):
    return render(request, "pets/pet-add-page.html")


def pet_details(request, pk):
    return render(request, "pets/pet-delete-page.html")


def pet_delete(request, pk):
    return render(request, "pets/pet-delete-page.html")


def pet_edit(request, pk):
    return render(request, "pets/pet-edit-page.html")
