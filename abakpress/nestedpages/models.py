from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    url = models.CharField(_('URL'), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(_('name'), max_length=100, db_index=True)
    head = models.CharField(_('head'), max_length=200)
    content = models.TextField(_('content'), blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('page', kwargs={'url': self.url})
