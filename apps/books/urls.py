from django.urls import path
from apps.books.views import (BooksListOrCreateView, BookImageView, BookDetailView, BookSearchView,
                              WishlistsView, WishlistsDeleteView, RateView, ReviewListOrCreateView,
                              ReviewDeleteView, HighBookRatingView, OrdersView, OrderRetriveView,
                              OrderCancelView, ChangeOrderStatusView, OrdersHistoryView)

urlpatterns = [
    path('books/', BooksListOrCreateView.as_view(), name='book-list'),
    path('books/<int:id>/upload-image/', BookImageView.as_view(), name='book-image'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/search/', BookSearchView.as_view(), name='book-search')
]

urlpatterns += [
    path('wishlist/', WishlistsView.as_view(), name='wishlist-list'),
    path('wishlist/<int:book_id>/', WishlistsDeleteView.as_view(), name='wishlist-delete'),
    path('books/<int:book_id>/reviews/', ReviewListOrCreateView.as_view(), name='reviews'),
    path('reviews/<int:pk>/', ReviewDeleteView.as_view(), name='reviews_delete'),
    path('books/<int:pk>/rate/', RateView.as_view(), name='rating'),
    path('books/top-rated/', HighBookRatingView.as_view(), name='top_rated_books')
]

urlpatterns += [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderRetriveView.as_view(), name='order-detail'),
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('orders/<int:pk>/status/', ChangeOrderStatusView.as_view(), name='order-status'),
    path('orders/history/', OrdersHistoryView.as_view(), name='orders-history')
]