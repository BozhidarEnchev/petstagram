from django.db import models

from petstagram.photos.models import Photo


class Comment(models.Model):
    comment_text = models.TextField(
        max_length=300,
    )

    datetime_of_publication = models.DateTimeField(
        auto_now_add=True,
    )


class Like(models.Model):
    to_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
