from sys import path

from django.db import models

from config import settings
from photostock.users.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=255)

    def get_count_category(self):
        return Picture.objects.filter(category=self.id).count()

    def __str__(self):
        return self.name


class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='images/')
    small_picture = ImageSpecField(source='picture',
                                      processors=[ResizeToFill(250, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



# pic = Picture.objects.all()[1]
# print(pic.small_picture.url)
# print(pic.small_picture.width)
