import hashlib
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import django.forms as forms

class FindingsArticle(models.Model):
    clipping = models.TextField()
    md5 = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=128, null=True, blank=True)
    isbn = models.CharField(max_length=12, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.md5 = hashlib.md5(self.clipping.encode('utf-8')).hexdigest()
        super(FindingsArticle, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.md5

class FindingsArticleForm(forms.ModelForm):
    class Meta:
        model = FindingsArticle
        fields = ['url','isbn','clipping']
