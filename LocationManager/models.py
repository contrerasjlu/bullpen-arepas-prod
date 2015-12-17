from django.db import models


class location_admin_menu(models.Model):
	label = models.CharField(max_length=50)
	url = models.CharField(max_length=50, null=True)
	imgClass = models.CharField(max_length=50, null=True)
	activeOn = models.CharField(max_length=20, null=True)
	order = models.IntegerField()
	child_of = models.CharField(max_length=20, null=True)
	
	def __unicode__(self):
		return self.label

	class Meta:
		verbose_name = "Menu Option"
		verbose_name_plural = "Menu Options"
