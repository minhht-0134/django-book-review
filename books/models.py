from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TimeStampMixin(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class ActivitiesMixin():
  def activities(self):
    model = self.__class__.__name__.lower()

    return Activity.objects.filter(
      target_object_id=self.id,
      target_object_type_id=ContentType.objects
        .get(app_label='books', model=model).id,
    )

class Author(TimeStampMixin):
  first_name = models.CharField(max_length=64)
  last_name = models.CharField(max_length=64)

  def __str__(self):
    return self.first_name + ' ' + self.last_name

  def full_name(self):
    return self.__str__()

class Category(TimeStampMixin):
  title = models.CharField(max_length=64)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name_plural = 'Categories'

class Book(ActivitiesMixin, TimeStampMixin):
  author = models.ForeignKey(
    Author,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
  )
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  title = models.CharField(max_length=64)
  pub_date = models.DateField()
  number_of_pages = models.IntegerField()

  def __str__(self):
    return self.title

  def reviews(self):
    return self.activities().filter(action_type=Activity.COMMENT)

class Activity(ActivitiesMixin, TimeStampMixin):
  RATE = 0
  COMMENT = 1
  READ = 2
  FAVORITE = 3
  FOLLOW = 4
  BUY = 5
  LIKE = 6
  ACTION_TYPE_CHOICES = [
    (RATE, 'Rate'),
    (COMMENT, 'Comment'),
    (READ, 'Read'),
    (FAVORITE, 'Favorite'),
    (FOLLOW, 'Follow'),
    (BUY, 'Buy'),
    (LIKE, 'Like'),
  ]

  READING = 0
  READED = 1
  READING_STATUSES = [
    (READING, 'Reading'),
    (READED, 'Readed'),
  ]

  BUY_PENDING = 0
  BUY_APPROVE = 1
  BUY_REJECT = 2
  BUY_STATUSES = [
    (BUY_PENDING, 'Pending'),
    (BUY_APPROVE, 'Approve'),
    (BUY_REJECT, 'Reject'),
  ]

  STATUSES = {
    'Read': READING_STATUSES,
    'Buy': BUY_STATUSES,
  }

  user = models.ForeignKey(User, on_delete=models.CASCADE)

  target_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  target_object_id = models.PositiveIntegerField()
  target_object = GenericForeignKey('target_object_type', 'target_object_id')

  action_type = models.PositiveSmallIntegerField(
    choices=ACTION_TYPE_CHOICES,
    default=RATE
  )
  status = models.PositiveSmallIntegerField(blank=True, null=True)
  content = models.TextField(blank=True, null=True)

  def comments(self):
    return self.activities().filter(action_type=Activity.COMMENT)

  def status_text(self):
    status_text = self.ACTION_TYPE_CHOICES[int(self.action_type)][1]

    try:
      return self.STATUSES[status_text][int(self.status)][1]
    except (KeyError, IndexError, TypeError):
      return status_text

  class Meta:
    verbose_name_plural = 'Activities'
    ordering = ['-created_at']
