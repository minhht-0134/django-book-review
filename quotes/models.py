from django.db import models

class Quote(models.Model):
    content = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)

