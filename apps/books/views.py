from django.shortcuts import render
from apps.books.serializers import BookSerializer, BookRatingSerializer, BookReviewSerializer, BookImgaeSerializer, WishlistSerializer, OrderSerializer
from apps.books.models import Book, BookRating, BookReview, BookImage, Wishlists, Orders
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from apps.books.permissions import IsOwnerOrAdmin
# Create your views here.


class BooksListOrCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookImageView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BookImgaeSerializer

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        serializer.save(book=book)


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    

class BookSearchView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author']


class WishlistsView(ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlists.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        book = serializer.validated_data.get('book')
        user =self.request.user

        if Wishlists.objects.filter(user=user, book=book).exists():
            return Response({'error': 'Bu kitob allaqachoin wishlistda mavjud!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=self.request.user)


class WishlistsDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlists.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        wishlist = Wishlists.objects.filter(user=self.request.user, book=book_id)

        if wishlist.exists():
            wishlist.delete()
            return Response({'success': 'Kitob wishlistdan o\'chirildi!'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Bu kitob wishlistda mavjud emas!'}, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewListOrCreateView(ListCreateAPIView):
    serializer_class = BookReviewSerializer

    def get_queryset(self):
        return super().get_queryset().filter(book=self.kwargs.get('book_id'))

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        serializer.save(book=book, user=self.request.user)


class ReviewDeleteView(DestroyAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [IsOwnerOrAdmin]
    queryset = BookReview.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': 'Review o\'chirildi!'}, status=status.HTTP_204_NO_CONTENT)
    

class RateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookRatingSerializer

    def get_queryset(self):
        book_id = self.kwargs.get("pk")
        return BookRating.objects.filter(book_id=book_id)
    
    def perform_create(self, serializer):
        book_id = self.kwargs.get("pk")
        book = Book.objects.filter(id = book_id)
        serializer.save(user=self.request.user, book=book)


class HighBookRatingView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BookRatingSerializer

    def get_queryset(self):
        return BookRating.objects.filter(rating_gt=2).order_by('-rating')
    


class OrdersView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetriveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated ,IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Orders.objects.none()
        return Orders.objects.filter(user=self.request.user)
    

class OrderCancelView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Orders.objects.none()
        return Orders.objects.filter(user=self.request.user, status='pending')

    def perform_update(self, serializer):
        serializer.instance.status = 'cancelled'
        serializer.save()


class ChangeOrderStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    
    def perform_update(self, serializer):
        new_status = self.request.data.get("status")
        if new_status not in ["pending", "paid", "cancelled"]:
            return Response({"error": "Notog'ri status"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.instance.status = new_status
        serializer.save()
        return Response({"success": "Status yangilandi"}, status=status.HTTP_200_OK)
    

class OrdersHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Orders.objects.all()
        return Orders.objects.filter(user=user)

        