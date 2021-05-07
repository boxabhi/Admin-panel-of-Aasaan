from django.db import models
from froala_editor.fields import FroalaField
from django.utils.text import slugify


class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class News(models.Model):
    title = models.TextField()
    content = FroalaField()
    slug = models.SlugField(null=True , blank=True)
    is_deleted = models.BooleanField(default =False)
    is_trending = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = NewsManager()
    admin_objects = models.Manager()

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)



