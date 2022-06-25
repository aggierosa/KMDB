from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from Movie.models import Movie
from Review.models import Review
from Review.serializer import ReviewSerializer
from .permissions import IsOwnerOrReadOnly


class ReviewView(APIView, PageNumberPagination):
    def get(self, request):
        reviews = Review.objects.all()

        result_page = self.paginate_queryset(reviews, request, self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
        # paginação

class ReviewDetailView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Filme não encontrado"}
            )

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, critic=request.user)

        return Response(serializer.data)

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Filme não encontrado"}
            )

        review = Review.objects.all().filter(movie_id=movie_id)

        result_page = self.paginate_queryset(review, request, self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

        # paginação

class ReviewDeleteSelfView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)

        except Movie.DoesNotExist:
            return Response(
                {"message": "Review não encontrada"}
            )

        review.delete()

        return Response(status.HTTP_204_NO_CONTENT)