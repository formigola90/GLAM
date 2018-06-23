#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


#class ContactQuerySet(models.QuerySet):
 #   def query_output(self, query):
  #      return self.filter(query)

class ContactType(models.Model):
	contact_type = models.CharField(max_length=100, default='Person')
	def __unicode__(self):        # __unicode__ on Python 2
	  return self.contact_type

class Nation (models.Model):
	nation = models.CharField(max_length=100)
	def __unicode__(self):        # __unicode__ on Python 2
	  return self.nation

class Region (models.Model):
	nation = models.ForeignKey(Nation)
	region = models.CharField(max_length=100)
	def __unicode__(self):        # __unicode__ on Python 2
	  return self.region

class Contact(models.Model):
    created_by = models.ForeignKey(User) #http://www.b-list.org/weblog/2006/nov/02/django-tips-auto-populated-fields/
	name = models.CharField(max_length=100)
    slug = models.SlugField()
	email = models.CharField(max_length=100, unique=True)
	phone = models.CharField(max_length=100, default='no phone')
	nation = models.ForeignKey(Nation)
	region = models.ForeignKey(Region)
	address = models.CharField(max_length=200, default='no address')
	contact_type = models.ForeignKey(ContactType)
	relationship_type = models.CharField(max_length=100, default='no relations')
	medium_payment = models.CharField(max_length=100, default='unknown')
	contact_month = models.CharField(max_length=100, default='unknown')
	other_info =  models.TextField(default='no other info')

	#objects = ContactQuerySet.as_manager()

        def get_absolute_url(self):
          return reverse("contact_detail", kwargs={"slug": self.slug})

	def __unicode__(self):        # __unicode__ on Python 2
	  return self.name

        def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Contact, self).save(*args, **kwargs)

class Story(models.Model):
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	date_of_dispatch = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=1000, default='contacted via standard html email')
	reply = models.BooleanField(default=False)
	via_phone_contact = models.BooleanField(default=False)
	via_social_contact = models.BooleanField(default=False)
	via_email_contact = models.BooleanField(default=False)
	
	def __unicode__(self):              # __unicode__ on Python 2
          return "%s contacted: %s" % (self.contact, self.date_of_dispatch)


