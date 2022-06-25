from rest_framework import serializers

from Genre.serializer import GenreSerializer
from .models import Movie
from Genre.models import Genre


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):

        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for g in genres:
            genre, _ = Genre.objects.get_or_create(**g)

            movie.genres.add(genre)      

        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.premiere = validated_data.get('premiere', instance.premiere)
        instance.classification = validated_data.get('classification', instance.classification)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
       
        instance.genres.clear()

        genres = validated_data.pop("genres")

        for g in genres:
            genre, _ = Genre.objects.get_or_create(**g)
            instance.genres.add(genre)
            
        instance.save()

        return instance