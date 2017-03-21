from __future__ import unicode_literals

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils.text import slugify

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='product_likes')
    modified_at = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("product:like-toggle", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-created_at", "-modified_at"]

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_product_receiver, sender=Product)
