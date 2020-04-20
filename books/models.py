from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_book(self):
        books = Book.objects.filter(category=self.id).count()
        return books
    
class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, null=False, blank=False)
    pages = models.IntegerField(default=0)
    score_rate = models.FloatField(default=0)
    total_rate = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='category_books', on_delete=models.CASCADE)
    image_src = models.ImageField(upload_to='static/uploads/images', null=True, blank=True, default="static/uploads/default.png")
    image_url = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_star(self):
        try:
            star = self.score_rate / self.total_rate
            total_star = format(star, '.1f')
            return total_star
        except:
            return "0.0"
    
class Rate(models.Model):
    user = models.ForeignKey(User, related_name='user_rate', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book_rate', on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=False)
    review = models.CharField(max_length=255, null=False, blank=False)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def make_range(self):
        return range(self.score)
    
    def get_create(self):
        day = self.updated.day
        month = self.updated.month
        year = self.updated.year
        create_at = f"{day}/{month}/{year}"
        return create_at