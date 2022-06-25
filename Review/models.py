from unicodedata import category
from django.db import models


class CategoryReview(models.TextChoices):
    MUSTWATCH = ("MW", "Must Watch")
    SHOULDWATCH = ("SW", "Should Watch")
    AVOIDWATCH = ("AW", "Avoid Watch")
    NOOPINION = ("NO", "No Opinion")

class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        null=True,
        max_length=50,
        choices=CategoryReview.choices,
        default=CategoryReview.NOOPINION
    )

    critic = models.ForeignKey('custom_user.User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie.Movie', on_delete=models.CASCADE)

