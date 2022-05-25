from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=False)
    placeholder_url = models.CharField(
        max_length=200,
        default="https://www.palomacornejo.com/wp-content/uploads/2021/08/no-image.jpg",
    )
