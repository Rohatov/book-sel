from django.urls import path
from apps.admins.views import UserListView, OrderListView, UserDeleteView, StatisticView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('stats/', StatisticView.as_view(), name='statistics' ),
]