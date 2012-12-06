from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class AccessToken(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access_token = models.CharField(max_length=64, unique=True)
    expires_in = models.IntegerField(default=0)
    refresh_token = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.access_token
