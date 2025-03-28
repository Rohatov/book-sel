from django.shortcuts import render
from apps.accounts.models import User
from apps.books.models import Orders, BookReview, Book, BookRating
from apps.accounts.serializers import UserSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count
from django.utils.timezone import now
# Create your views here.

class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OrderListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = Orders.objects.all()


class StatisticView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = now().date()

        stats = {
            "users": {
                "total_users": User.objects.count(),
                "added_today": User.objects.filter(date_joined__date=today).count(),
                "admins": User.objects.filter(is_staff=True).count(),
            },
            "orders": {
                "total_orders": Orders.objects.count(),
                "completed_orders": Orders.objects.filter(status="paid").count(),
                "pending_orders": Orders.objects.filter(status="pending").count(),
                "canceled_orders": Orders.objects.filter(status="cancelled").count(),
                "total_revenue": Orders.objects.filter(status="paid").aggregate(Sum('total_price'))['total_price__sum'] or 0,
                "top_selling_book": Orders.objects.values('book__title').annotate(total_sales=Count('id')).order_by('-total_sales').first(),
            },
            "books": {
                "total_books": Book.objects.count(),
                "added_today": Book.objects.filter(date_added__date=today).count(),
                "top_rated_book": Book.objects.values('book__title').annotate(average_rating=Avg('book__rating')).order_by('-average_rating').first(),
            },
            "reviews": {
                "total": BookRating.objects.aggregate(Sum('rating'))['rating__sum'] or 0,
                "new_today": Book.objects.filter(created_at__date=today).count(),
                "most_reviewed_book": Book.objects.annotate(review_count=Count('ratings')).order_by('-review_count').first(),
            },
        }

