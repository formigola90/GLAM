# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Contact
from .models import Story
from .models import Nation
from .models import Region
from .models import ContactType
from .models import Feedback
from .models import Profile


admin.site.register(ContactType)
admin.site.register(Region)
admin.site.register(Nation)
admin.site.register(Contact)#, ContactAdmin)
admin.site.register(Story)
admin.site.register(Feedback)
admin.site.register(Profile)