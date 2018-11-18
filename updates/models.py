from django.conf import settings
from django.db import models


def upload_update_image(instance, filename):
    return "updates/{user}/filename".format(user=instance.user, filename=filename)


# Create your models here.
class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CharField)
    title = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to=upload_update_image, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
