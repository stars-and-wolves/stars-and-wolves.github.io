"""
3 step guide to changing models:
	1. change models
	2. cmd-line: python manage.py makemigrations
	3. cmd-line: python manage.py migrate
"""

from django.db import models
from datetime import datetime as dt

# Create your models here.
class MoonRequest(models.Model):
	# DateField('x') would give human-readable name but variables are human readable anyway
	start_date = models.DateField()
	end_date = models.DateField()
	request_date = models.DateTimeField()

	def __str__(self):
		return (self.dt_pretty_print(self.start_date) + " to " + self.dt_pretty_print(self.end_date))

	def dt_pretty_print(self, d):
		year_s = d.strftime("%Y")
		month_s = d.strftime("%b")
		day_s = d.strftime("%d")
		if d.day < 10:
			day_s = day_s.replace("0", " ")
		weekday_s = d.strftime("%a")
		date_s = (year_s + " " + month_s + " " + day_s + " (" + weekday_s + " night)")
		return date_s
	#end dt_prettyprint()
