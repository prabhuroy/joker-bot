from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserData(models.Model):
	userid = models.CharField(max_length=100,null=True,blank=True)
	user_name = models.CharField(max_length=100,null=True,blank=True)
	stupid_count = models.IntegerField(default=0)
	fat_count    = models.IntegerField(default=0)
	dumb_count   = models.IntegerField(default=0)

	def __str__(self):
		return str(self.userid)