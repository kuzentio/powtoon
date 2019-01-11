from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models


class Powtoon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    content = JSONField(default=dict)
    shared_with = models.ManyToManyField(User, related_name='shared')

    class Meta:
        permissions = (
            ("can_share", "Can share any Powtoons"),
            ("can_see", "Can see any Powtoons"),
        )
