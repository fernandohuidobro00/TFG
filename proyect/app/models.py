from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class Attribute(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    attribute_key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        
        db_table = 'attribute'
        managed = True


class Business(models.Model):
    business_id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    stars = models.FloatField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    is_open = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'business'
        managed = True


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=255, blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    yelping_since = models.DateTimeField(blank=True, null=True)
    useful = models.IntegerField(blank=True, null=True)
    funny = models.IntegerField(blank=True, null=True)
    cool = models.IntegerField(blank=True, null=True)
    fans = models.IntegerField(blank=True, null=True)
    average_stars = models.FloatField(blank=True, null=True)
    compliment_hot = models.IntegerField(blank=True, null=True)
    compliment_more = models.IntegerField(blank=True, null=True)
    compliment_profile = models.IntegerField(blank=True, null=True)
    compliment_cute = models.IntegerField(blank=True, null=True)
    compliment_list = models.IntegerField(blank=True, null=True)
    compliment_note = models.IntegerField(blank=True, null=True)
    compliment_plain = models.IntegerField(blank=True, null=True)
    compliment_cool = models.IntegerField(blank=True, null=True)
    compliment_funny = models.IntegerField(blank=True, null=True)
    compliment_writer = models.IntegerField(blank=True, null=True)
    compliment_photos = models.IntegerField(blank=True, null=True)
    friends = ArrayField(models.CharField(max_length=255))
    elite_years = ArrayField(models.IntegerField())

    class Meta:
        
        db_table = 'user'
        managed = True


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'category'
        managed = True


class Checkin(models.Model):
    date = models.CharField(max_length=255)
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'checkin'
        managed = True



class Review(models.Model):
    review_id = models.CharField(primary_key=True, max_length=22)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, blank=True, null=True)
    stars = models.FloatField(blank=True, null=True)
    useful = models.IntegerField(blank=True, null=True)
    funny = models.IntegerField(blank=True, null=True)
    cool = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'review'
        managed = True


class Hours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    opening_time = models.TimeField(default=datetime.time(9,30))
    closing_time = models.TimeField(default=datetime.time(22,00))

    class Meta:
        
        db_table = 'hours'
        managed = True


class Tip(models.Model):
    tip_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    compliment_count = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'tip'
        managed = True



