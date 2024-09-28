from django.urls import path

import petstagram.accounts.views

urlpatterns = [
    path('', petstagram.accounts.views.register)
]