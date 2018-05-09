from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse

from .utils import create_shortcode
from .validators import validate_url, validate_dot_com

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)


class ShortishURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ShortishURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)  # used to filter only active shortcodes
        return qs

    def refresh_shortcodes(self, items=None):
        qs = ShortishURL.objects.filter(id__gte=1)  # gte means greater than or equal to
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class ShortishURL(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)  # everytime the model is saved, its gonna set that time
    timestamp = models.DateTimeField(auto_now_add=True)  # when model was created, its gonna set that time
    active = models.BooleanField(default=True)

    objects = ShortishURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        # if not "http" in self.url:
        #     self.url = "http://" + self.url
        super(ShortishURL, self).save(*args, **kwargs)

    # class Meta:
    #     ordering = '-id'

    # def my_save(self):    # we can override default save method by our custom "my_save" method
    #    self.save()

    def __str__(self):          # in case of python 3
        return str(self.url)

    def __unicode__(self):      # in case of python 2
        return str(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host="www", scheme="http")
        return url_path
