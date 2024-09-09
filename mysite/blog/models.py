from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

# Create your models here.
# By default, Django adds an auto-incrementing primary key field to each model. The field type for this field is specified in each application configuration or globally in the DEFAULT_AUTO_FIELD setting. When creating an application with the startapp command, the default value for DEFAULT_AUTO_FIELD is BigAutoField. This is a 64-bit integer that automatically increments according to available IDs. If you don’t specify a primary key for your model, Django adds this field automatically. You can also define one of the model fields to be the primary key by setting primary_key=True on it.
class Post(models.Model):
    tags = TaggableManager()


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    # https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.on_delete possible option s for on_delete options
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # class named status has been defined to give user option to choose if it is a draft or published
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
    )
    objects = models.Manager() #the default manager
    published = PublishedManager() # Our customer manager

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )



class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'