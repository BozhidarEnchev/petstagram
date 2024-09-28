# Generated by Django 5.1.1 on 2024-09-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pets", "0003_alter_pet_slug"),
        ("photos", "0002_alter_photo_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="tagged_pets",
            field=models.ManyToManyField(blank=True, null=True, to="pets.pet"),
        ),
    ]
