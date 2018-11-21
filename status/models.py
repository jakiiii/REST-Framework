from django.conf import settings
from django.db import models


class StatusQuerySet(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self.db)


def upload_status_image(instance, filename):
    return "status/{user}{filename}/".format(user=instance.user, filename=filename)


# Create your models here.
class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_status_image, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = StatusManager()

    def __str__(self):
        return str(self.content)[:50] or "----- Blank content -----"

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Posts'
