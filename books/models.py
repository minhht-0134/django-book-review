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
    publish_date = models.DateTimeField()
    author = models.CharField(max_length=255, null=False, blank=False)
    pages = models.IntegerField(default=0)
    score_rate = models.FloatField(default=0)
    total_rate = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='category_books', on_delete=models.CASCADE)
    image_src = models.ImageField(upload_to='static/uploads/images', null=True, blank=True,
                                  default="static/uploads/default.png")
    image_url = models.CharField(max_length=255, null=True, blank=False)
    book_url = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_star(self):
        try:
            star = self.score_rate / self.total_rate
            total_star = format(star, '.1f')
            return total_star
        except:
            return "0.0"
    
    def get_publist(self):
        day = self.publish_date.day
        month = self.publish_date.month
        year = self.publish_date.year
        publish = f"{day}/{month}/{year}"
        return publish
    
    def trunc_title(self):
        trunc = self.title
        if len(trunc)>20:
            return trunc[0:20] + "..."
        else:
            return trunc
        


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
    
    def list_comment(self):
        comments = []
        try:
            comments = self.rate_comment.all().order_by('-id')
        except:
            print('err')
            return comments
        return comments
    
    def count_comment(self):
        count = 0
        try:
            count = self.rate_comment.all().count()
        except:
            print('err')
            return count
        return count


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, related_name='rate_comment', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_create(self):
        day = self.updated.day
        month = self.updated.month
        year = self.updated.year
        minute = self.updated.minute
        hour = self.updated.hour
        create_at = f"on {day}/{month}/{year} at {hour}:{minute}"
        return create_at
    
    def trunc_cmt(self):
        trunc = self.content
        if len(trunc)>50:
            return trunc[0:50] + "..."
        else:
            return trunc

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='user_favorite', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book_favorite', on_delete=models.CASCADE)


class Action(models.Model):
    ACTION_CHOICES = [
        ('add', 'added'),
        ('rated', 'rated'),
        ('edited', 'edited'),
        ('responded', 'responded'),
        ('deleted', 'deleted'),
        ('removed', 'removed'),
    ]
    user = models.ForeignKey(User, related_name='user_action', on_delete=models.CASCADE)
    time_action = models.DateTimeField(auto_now_add=True)
    content_action = models.CharField(max_length=255, null=False, blank=False)
    link_action = models.CharField(max_length=255, null=True, blank=False)
    type_action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )
    
    def get_time(self):
        day = self.time_action.day
        month = self.time_action.month
        year = self.time_action.year
        minute = self.time_action.minute
        hour = self.time_action.hour
        time_action = f"on {day}/{month}/{year} at {hour}:{minute}"
        return time_action


class MarkBook(models.Model):
    MARK_CHOICES = [
        ('read', 'read'),
        ('reading', 'reading'),
    ]
    user = models.ForeignKey(User, related_name='user_mark', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book_mark', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=MARK_CHOICES
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class RequestBook(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('canceled', 'canceled'),
    ]
    user = models.ForeignKey(User, related_name='user_request', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book_request', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    content = models.CharField(max_length=255, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
