from django.db import models
from taggit.managers import TaggableManager

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = TaggableManager()
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#     class Meta:
#         ordering = ['-created_at']
