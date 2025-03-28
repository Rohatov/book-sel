from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.config.models import Basemodel
from apps.accounts.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class Book(Basemodel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class BookImage(Basemodel):
    image = models.ImageField(upload_to='images/')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')


class BookReview(Basemodel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return self.review


class BookRating(Basemodel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.book.title} - {self.rating}"
    

class Wishlists(Basemodel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    

class Orders(Basemodel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        self.total_price = self.book.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.quantity} - {self.total_price}"
