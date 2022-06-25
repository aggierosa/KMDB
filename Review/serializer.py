from dataclasses import fields
from rest_framework import serializers

from Movie.models import Movie
from .models import Review
from Movie.serializer import MovieSerializer
from custom_user.models import User


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers', 'recomendation', 'movie_id', 'critic']
        extra_kwargs = {'stars': {'min_value': 1, 'max_value': 10}}
