from django.db import models
from django.db.models import DO_NOTHING


class InviteCode(models.Model):
    code = models.CharField(max_length=6)


class User(models.Model):
    number = models.CharField(max_length=11)
    generated_code = models.ForeignKey('InviteCode', on_delete=DO_NOTHING, related_name='generated_code')
    applied_code = models.ForeignKey('InviteCode', on_delete=DO_NOTHING, related_name='applied_code', null=True)
