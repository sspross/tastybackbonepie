from django.db import models


class Book(models.Model):
	name = models.CharField(max_length=50)
	added = models.DateField()
	read = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name