from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^contact_form$', views.FilterFormView.as_view(), name='contact_form'),
                url(r'^$', views.index, name='index'),
                url(r'^contact_detail/(?P<slug>\S+)/$', views.contact_view, name='contact_detail'),
                url(r'^user_profile/(?P<username>\S+)/$', views.user_profile, name='user_profile'),
                url(r'^contact_send/(?P<slug>\S+)$', views.send, name='send'),
                url(r'^add_contact_1$', views.AddContactFormView.as_view(), name='add_contact'),
               # url(r'^add_contact_2/(?P<nation>\S+)/(?P<contact_type>\S+)/$', views.add_contact_2, name='add_contact_2'),
                url(r'^contact_send_to_list/$', views.send_to_list, name='send_to_list')]