from django.contrib import admin
from petstagram.pets.models import Pet


@admin.register(Pet)
class AdminPet(admin.ModelAdmin):
    list_display = ['name', 'slug']
