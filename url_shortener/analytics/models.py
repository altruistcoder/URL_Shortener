from django.db import models
from shortish.models import ShortishURL


class ClickEventManager(models.Manager):
    def create_event(self, ShortishInstance):
        if isinstance(ShortishInstance, ShortishURL):
            obj, created = self.get_or_create(Shortish_url=ShortishInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    Shortish_url = models.OneToOneField(ShortishURL)
    count        = models.IntegerField(default=0)
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
