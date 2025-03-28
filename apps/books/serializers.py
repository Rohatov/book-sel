from rest_framework import serializers
from apps.accounts.models import User
from apps.books.models import Book, BookImage, BookRating, BookReview, Wishlists, Orders


class BookImgaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'


class BookRatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BookRating
        fields = ['id', 'user', 'rating']


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'review', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    images = BookImgaeSerializer(many=True, read_only=True)
    ratings = BookRatingSerializer(many=True, read_only=True)
    reviews = BookReviewSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'owner', 'images', 'reviews', 'ratings']


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Wishlists
        fields = ['id', 'user', 'book']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Orders
        fields = ['id', 'user', 'book', 'quantity', 'total_price']