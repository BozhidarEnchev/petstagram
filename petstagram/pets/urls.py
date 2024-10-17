from django.urls import path, include

from petstagram.pets import views
from petstagram.pets.views import PetDetailsView, AddPetView

urlpatterns = [
    path('add/', AddPetView.as_view(), name='add-pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', PetDetailsView.as_view(), name='pet-details'),
        path('edit/', views.pet_edit_page, name='edit-pet'),
        path('delete/', views.pet_delete_page, name='delete-pet'),
    ]))
]