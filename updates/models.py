import json
from django.conf import settings
from django.db import models
from django.core.serializers import serialize


class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     return serialize('json', qs, fields=['user', 'title', 'image', 'content'])

    # def serialize(self):
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         structure = json.loads(obj.serialize())
    #         final_array.append(structure)
    #     return json.dumps(final_array)

    def serialize(self):
        list_values = list(self.values('id', 'user', 'title', 'image', 'content'))
        return json.dumps(list_values)


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, using=self._db)


def upload_update_image(instance, filename):
    return "updates/{user}/filename".format(user=instance.user, filename=filename)


# Create your models here.
class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CharField)
    title = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to=upload_update_image, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UpdateManager()

    def __str__(self):
        return self.title

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""
        data = {
            "id": self.id,
            "user": self.user.id,
            "title": self.title,
            "image": image,
            "content": self.content
        }
        data = json.dumps(data)
        return data
