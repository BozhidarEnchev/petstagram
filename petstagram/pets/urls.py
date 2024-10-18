from django.urls import path, include

from petstagram.pets import views
from petstagram.pets.views import PetDetailsView, AddPetView, EditPetView, DeletePetView

urlpatterns = [
    path('add/', AddPetView.as_view(), name='add-pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', PetDetailsView.as_view(), name='pet-details'),
        path('edit/', EditPetView.as_view(), name='edit-pet'),
        path('delete/', DeletePetView.as_view(), name='delete-pet'),
    ]))
]