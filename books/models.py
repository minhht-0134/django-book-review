from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    
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