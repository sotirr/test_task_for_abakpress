import re

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

    def convert_to_html(self, site_name):
        regex_bold = r'\*\*(.+?)\*\*'
        regex_italic = r'\\\\(.+?)\\\\'
        regex_link = r'\(\((.+?) (.+?)\)\)'
        replace_bold = r'<b>\1</b>'
        replace_italic = r'<i>\1</i>'
        replace_link = r'<a href="http://' + site_name + r'/\1">\2</a>'
        replaced_bold = re.sub(regex_bold, replace_bold, self.content)
        replaced_italic = re.sub(regex_italic, replace_italic, replaced_bold)
        replaced_link = re.sub(regex_link, replace_link, replaced_italic)
        return replaced_link
