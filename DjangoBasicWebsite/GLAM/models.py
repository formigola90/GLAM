#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime


class ContactType(models.Model):
	contact_type = models.CharField(max_length=100, default='Person')
	def __str__(self):
	    return self.contact_type

class Nation (models.Model):
	nation = models.CharField(max_length=100)
	def __str__(self):
	    return self.nation

class Region (models.Model):
	nation = models.ForeignKey(Nation)
	region = models.CharField(max_length=100)
	def __str__(self):
	    return self.region

class Contact(models.Model):
    # #http://www.b-list.org/weblog/2006/nov/02/django-tips-auto-populated-fields/
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, default='no phone')
    nation = models.ForeignKey(Nation)
    region = models.ForeignKey(Region)
    address = models.CharField(max_length=200, default='no address')
    contact_type = models.ForeignKey(ContactType)
    website =  models.URLField(max_length=1000, default='www.I_Have_No_Website.none')
    created_by = models.ForeignKey(User)
    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"slug": self.slug})
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        i=1
        while (i <= Contact.objects.filter(slug=self.slug).count()):
            if (Contact.objects.filter(slug=self.slug)[0]!= self):
                self.slug=self.slug+slugify(self.name)
            i=i+1
        super(Contact, self).save(*args, **kwargs)


class Story(models.Model):
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	date_of_dispatch = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=1000, default='contacted via standard html email')
	reply = models.BooleanField(default=False)
	via_phone_contact = models.BooleanField(default=False)
	via_social_contact = models.BooleanField(default=False)
	via_email_contact = models.BooleanField(default=False)
	
	def __str__(self):
	    return "%s contacted: %s" % (self.contact, self.date_of_dispatch)

class Feedback(models.Model): #https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-choices
        STRUNRAC = 'SU'
        UNRAC = 'UN'
        NEUTRAL = 'NE'
        RACOM = 'RA'
        STRRAC = 'SR'
        RATING_CHOICES = (
           (STRUNRAC, 'Strongly Unrecommended'),
           (UNRAC, 'Unrecommended'),
           (NEUTRAL, 'Neutral'),
           (RACOM, 'Recommended'),
           (STRRAC, 'Strongly Recommended'),
        )
        contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        time_stamp = models.DateTimeField(auto_now_add=True)
        rating = models.CharField(
           max_length=2,
           choices=RATING_CHOICES,
           default=NEUTRAL
        )
        comment = models.TextField()
        def __str__(self):              # __unicode__ on Python 2
           return "%s rated %s as %s" % (self.created_by, self.contact, self.rating)
           
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    last_review_timestamp = models.DateField(default=datetime.date.today)
    last_database_add = models.DateField(default=datetime.date.today)
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()