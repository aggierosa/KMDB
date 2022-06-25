from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .models import Movie
from Movie.serializer import MovieSerializer


class MovieView(APIView, PageNumberPagination):

    def get(self, request):
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request, self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

        # paginação

class MovieViewDetail(APIView):

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Filme não encontrado"}
            )

        serializer = MovieSerializer(movie)

        return Response(serializer.data)


class MovieViewAuth(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)    


class MovieViewDetailAuth(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Filme não encontrado"}
            )

        self.check_object_permissions(request, movie)

        serializer = MovieSerializer(movie, request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Filme não encontrado"}
            )

        movie.delete()

        return Response(status.HTTP_204_NO_CONTENT)


