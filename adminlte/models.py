from django.db import models

# Create your models here.


class Worlddata(models.Model):
    confirmed = models.BigIntegerField(null=True, blank=True)
    deaths = models.BigIntegerField(null=True, blank=True)
    recovered = models.BigIntegerField(null=True, blank=True)
    date = models.DateField()


class Indiadata(models.Model):
    confirmed = models.BigIntegerField(null=True, blank=True)
    deaths = models.BigIntegerField(null=True, blank=True)
    recovered = models.BigIntegerField(null=True, blank=True)
    week = models.CharField(max_length=500)
    date = models.DateField()


class Countrydata(models.Model):
    country_id = models.IntegerField(default=0)
    confirmed = models.BigIntegerField(null=True, blank=True)
    deaths = models.BigIntegerField(null=True, blank=True)
    recovered = models.BigIntegerField(null=True, blank=True)
    date = models.DateField()


class Country(models.Model):
    cname = models.CharField(max_length=100)


class Dailydata(models.Model):
    country_id = models.IntegerField(default=0)
    cases = models.BigIntegerField(null=True)
    date =  models.DateField()

