from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from . import models
from .models import Contact, Nation, Region, Story, ContactType, Feedback, Profile
from django.template import loader
from .mail_smtp import send_mail
from .forms import contacts_filter_form, AddContactForm, FeedbackForm, AddContactForm_1, AddContactForm_2, FilterForm_1
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.forms import Textarea
import datetime

from django.contrib.auth.models import User

# the list of all contacts divided by contact_type
@login_required
def index(request):
    current_user = User.objects.get(username=request.user.username)
    contacts_list = Contact.objects.all()
    contacts_list = Contact.objects.order_by('-contact_type')
    template = loader.get_template('contacts/index.html')
    context = {
        'contacts_list': contacts_list,
        'current_user' : current_user,
    }
    return HttpResponse(template.render(context, request))

# the detail of the mail that's gonna be send to the contact
@login_required
def contact_detail(request, slug):
    current_user = User.objects.get(username=request.user.username)
    slug = str(slug)
    slug = slug.replace('/send','')
    slug = slug.replace("'u",'')
    contact = Contact.objects.get(slug=slug)
    template = loader.get_template('contacts/contact_details/contact_view.html')#('contacts/email_detail.html')
    context = {
        'contact': contact,
        'current_user' : current_user,
    }
    return HttpResponse(template.render(context, request))

# send the email and dysplay the sended mail
@login_required
def send(request, slug):
    current_user = User.objects.get(username=request.user.username)
    pwd="piantalaconstibonghi"
    contact = Contact.objects.get(slug=slug)
    template = loader.get_template('contacts/email_send.html')
    context = {
        'contact': contact,
        'current_user' : current_user,
    }
    html=HttpResponse(template.render(context, request))
    html=str(html.content)
    destination = contact
    send_mail(html, destination)
    return HttpResponse(template.render(context, request))

# send the email to a list of contacts
@login_required
def send_to_list(request):
  req = request.POST
  print(req)
  contacts_list = req.getlist("contact")
  sended_to = []

  for i in contacts_list:
    contact = Contact.objects.get(slug=i)
    sended_to.append(contact)
    template = loader.get_template('contacts/email_send.html')
    context = {
        'contact': contact,
        'current_user' : current_user,
    }
    html=HttpResponse(template.render(context, request))
    html=str(html.content)
    destination = contact
    send_mail(html, destination)
  template = loader.get_template('contacts/resoconto.html')
  context = {
        'contacts': sended_to,
        'current_user' : current_user,
    }
  return HttpResponse(template.render(context, request))
 
# form view
@login_required
def filtrati(request):
    current_user = User.objects.get(username=request.user.username)
    if request.method == 'GET':
        form = contacts_filter_form()
    else:
        # A POST request: Handle Form Upload
        # Bind data from request.POST into a PostForm
        form = contacts_filter_form(request.POST)
        # If data is valid, proceeds to create a new post and redirect the user
       
        if form.is_valid():
            pwd=form.cleaned_data['pwd']
            new_contacts = []
            contacts = Contact.objects.all()
            #print "name: "
            #print form.cleaned_data['name']
            if form.cleaned_data['name'] != '':
                filter_list = Contact.objects.filter(name = form.cleaned_data['name'])
                for i in contacts:
                    for j in filter_list:
                        if i == j:
                            new_contacts.append(i)
                contacts=new_contacts
                new_contacts = []
            #print "nation: "
            #print form.cleaned_data['nation']
            if form.cleaned_data['nation'] != None:
                filter_list = Contact.objects.filter(nation = Nation.objects.filter(nation=form.cleaned_data['nation']))
                for i in contacts:
                    for j in filter_list:
                        if i == j:
                            new_contacts.append(i)
                contacts=new_contacts
                new_contacts = []
            #print "region: "
            #print form.cleaned_data['region']
            if form.cleaned_data['region'] != None:
                filter_list = Contact.objects.filter(region = Region.objects.filter(region=form.cleaned_data['region']))
                for i in contacts:
                    for j in filter_list:
                        if i == j:
                            new_contacts.append(i)
                contacts=new_contacts
                new_contacts = []
            #print "contact type: " 
            #print  form.cleaned_data['contact_type']
            if form.cleaned_data['contact_type'] != None:
                filter_list = Contact.objects.filter(contact_type = ContactType.objects.filter(contact_type=form.cleaned_data['contact_type']))
                for i in contacts:
                    for j in filter_list:
                        if i == j:
                            new_contacts.append(i)
                contacts=new_contacts
                new_contacts = []
            other_contacts = []
            #print "contacted before: "
            #print form.cleaned_data['contacted_before']          
            if form.cleaned_data['contacted_before'] != None:
                #print form.cleaned_data['contacted_before']
                filter_list = Story.objects.all()
                #print filter_list
                for i in contacts:
                    for j in filter_list:
                        if i == j.contact:
                            if j.date_of_dispatch > form.cleaned_data['contacted_before']:
                                e=0
                                if other_contacts == []:
                                    other_contacts.append(i)
                                for k in new_contacts:
                                    if k == j.contact:
                                        e = 1
                                        break
                                if e==0:
                                    other_contacts.append(i)
                                    e=e+1
# ora la variabile other_contacts contiene tutti i contatti contattati dopo la data impostata, ora non resta che rimuovere questo gruppo di contatti dai contatti ragruppati nella variabile contacts
                for i in contacts:
                    e=0
                    for j in other_contacts:
                        if i == j:
                            e=1
                    if e==0:
                        new_contacts.append(i)
                contacts=new_contacts
                new_contacts = []
            template = loader.get_template('contacts/list.html')    
            context = {
                'list': contacts,
                'current_user' : current_user,
                'pwd': pwd
            }
            return HttpResponse(template.render(context, request)) 
    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'current_user' : current_user,
    })  
            
class FilterFormView(View):
    form_1 = FilterForm_1()
    form_2 = contacts_filter_form()
    initial = {'nation' : 'NONE',
               'contact_type':'NONE',}
    template_name = 'contacts/contact_form.html'

    def get(self, request, *args, **kwargs):
        current_user = User.objects.get(username=request.user.username)
        return render(request, self.template_name, {
            'form': self.form_1,
            'current_user' : current_user,
            })

    def post(self, request, *args, **kwargs):
        current_user = User.objects.get(username=request.user.username)
        if self.initial['nation']=='NONE':
            self.form_1 =  FilterForm_1(request.POST)
            if self.form_1.is_valid():
                self.initial['nation']=Nation.objects.get(nation=self.form_1.cleaned_data['nation'])
                self.initial['contact_type']=ContactType.objects.get(contact_type=self.form_1.cleaned_data['contact_type'])
                self.form_2= contacts_filter_form(initial=self.initial)
                self.form_2.fields["region"].queryset = Region.objects.filter(nation=self.initial['nation'])
                return render(request, self.template_name, {'form': self.form_2,
                    'current_user' : current_user,})
        else:
            self.form_2= contacts_filter_form(request.POST)
            if self.form_2.is_valid():
                new_contacts = []
                contacts = Contact.objects.all()
                if self.form_2.cleaned_data['name'] != '':
                    filter_list = Contact.objects.filter(name = self.form_2.cleaned_data['name'])
                    for i in contacts:
                        for j in filter_list:
                            if i == j:
                                new_contacts.append(i)
                    contacts=new_contacts
                    new_contacts = []
                if self.form_2.cleaned_data['nation'] != None:
                    filter_list = Contact.objects.filter(nation = Nation.objects.filter(nation=self.form_2.cleaned_data['nation']))
                    for i in contacts:
                        for j in filter_list:
                            if i == j:
                                new_contacts.append(i)
                    contacts=new_contacts
                    new_contacts = []
                if self.form_2.cleaned_data['region'] != None:
                    filter_list = Contact.objects.filter(region = Region.objects.filter(region=self.form_2.cleaned_data['region']))
                    for i in contacts:
                        for j in filter_list:
                            if i == j:
                                new_contacts.append(i)
                    contacts=new_contacts
                    new_contacts = []
                if self.form_2.cleaned_data['contact_type'] != None:
                    filter_list = Contact.objects.filter(contact_type = ContactType.objects.filter(contact_type=self.form_2.cleaned_data['contact_type']))
                    for i in contacts:
                        for j in filter_list:
                            if i == j:
                                new_contacts.append(i)
                    contacts=new_contacts
#                    new_contacts = []
 #               other_contacts = []        
  #              if self.form_2.cleaned_data['contacted_before'] != None:
   #                 filter_list = Story.objects.all()
    #                for i in contacts:
     #                   for j in filter_list:
      #                      if i == j.contact:
       #                         if j.date_of_dispatch > self.form_2.cleaned_data['contacted_before']:
        #                            e=0
         #                           if other_contacts == []:
          #                              other_contacts.append(i)
           #                         for k in new_contacts:
            #                            if k == j.contact:
             #                               e = 1
              #                              break
               #                     if e==0:
                #                        other_contacts.append(i)
                 #                       e=e+1
    # ora la variabile other_contacts contiene tutti i contatti contattati dopo la data impostata, ora non resta che rimuovere questo gruppo di contatti dai contatti ragruppati nella variabile contacts
                  #  for i in contacts:
                   #     e=0
                    #    for j in other_contacts:
                     #       if i == j:
                      #          e=1
                       # if e==0:
                        #    new_contacts.append(i)
                    #contacts=new_contacts
                    new_contacts = []
                template = loader.get_template('contacts/list.html')    
                context = {
                    'list': contacts,
                    'current_user' : current_user,
                }
                return HttpResponse(template.render(context, request)) 
            return render(request, 'contacts/contact_details/contact_view.html', {
                    'current_user' : current_user,
                    'contact' : self.c
                    })
        return render(request, self.template_name, {'form': self.form_1,
            'current_user' : current_user,
            })


    
@login_required
def user_profile(request, username):
    current_user = User.objects.get(username=request.user.username)
    name = str(username)
    name = name.replace('/send','')
    name = name.replace("'u",'')
    profile = Profile.objects.get(user=User.objects.get(username=name))
    contacts_list = Contact.objects.filter(created_by=profile.user)
    reviews_list = Feedback.objects.filter(created_by=profile.user).order_by('-time_stamp')
    template = loader.get_template('registration/user_profile.html')
    context = {
        'current_user' : current_user,
        'reviews_list' : reviews_list,
        'last_review' : reviews_list[0],
        'contacts_list' : contacts_list,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))
    
    
class AddContactFormView(View):
    form_1 = AddContactForm_1()
    form_2 = AddContactForm()
    initial = {'nation' : 'NONE',
               'contact_type':'NONE',
               'email':'NONE',
               'name':'NONE',}
    template_name = 'contacts/add_contact.html'
    c = Contact()

    def get(self, request, *args, **kwargs):
        current_user = User.objects.get(username=request.user.username)
        return render(request, self.template_name, {
            'form': self.form_1,
            'current_user' : current_user,
            })

    def post(self, request, *args, **kwargs):
        current_user = User.objects.get(username=request.user.username)
        if self.initial['nation']=='NONE':
            self.form_1 = AddContactForm_1(request.POST)
            if self.form_1.is_valid():
                self.initial['nation']=Nation.objects.get(nation=self.form_1.cleaned_data['nation'])
                self.initial['contact_type']=ContactType.objects.get(contact_type=self.form_1.cleaned_data['contact_type'])
                self.initial['email']=self.form_1.cleaned_data['email']
                self.initial['name']=self.form_1.cleaned_data['name']
                self.form_2= AddContactForm(initial=self.initial)
                self.form_2.fields["region"].queryset = Region.objects.filter(nation=self.initial['nation'])
                return render(request, self.template_name, {'form': self.form_2,
                    'current_user' : current_user,})
        else:
            self.form_2= AddContactForm(request.POST)
            if self.form_2.is_valid():
                self.c = Contact(name = self.form_2.cleaned_data['name'],
                            nation = Nation.objects.filter(nation=self.form_2.cleaned_data['nation'])[0] ,
                            contact_type = ContactType.objects.filter(contact_type=self.form_2.cleaned_data['contact_type'])[0],
                            email = self.form_2.cleaned_data['email'],
                            website = self.form_2.cleaned_data['website'],
                            region = Region.objects.filter(region=self.form_2.cleaned_data['region'])[0],
                            address = self.form_2.cleaned_data['address'],
                            phone = self.form_2.cleaned_data['phone'],
                            created_by = current_user)
                self.c.save()
                current_profile = Profile.objects.get(user=current_user)
                current_profile.last_database_add=datetime.datetime.now()
                current_profile.save()
            return render(request, 'contacts/contact_details/contact_view.html', {
                    'current_user' : current_user,
                    'contact' : self.c
                    })
        return render(request, self.template_name, {'form': self.form_1,
            'current_user' : current_user,
            })
    
    
@login_required
def contact_view(request, slug):
    slug = str(slug)
    slug = slug.replace('/send','')
    slug = slug.replace("'u",'')
    contact = Contact.objects.get(slug=slug)
    reviews_list = Feedback.objects.filter(contact = contact).order_by('-time_stamp')
    template = loader.get_template('contacts/contact_details/contact_view.html')
    current_user = User.objects.get(username=request.user.username)
    
    if request.method == 'GET':
        form = FeedbackForm()
    else:
        # A POST request: Handle Form Upload
        # Bind data from request.POST into a PostForm
        form = FeedbackForm(request.POST)
        # If data is valid, proceeds to create a new post and redirect the user
       
        if form.is_valid():
            
            
            
            
            c = Feedback(
                        contact = contact,
                        created_by = current_user,
                        rating = form.cleaned_data['rating'],
                        comment = form.cleaned_data['comment'],
                        )
            c.save()
            form = FeedbackForm()
            current_profile = Profile.objects.get(user=current_user)
            current_profile.last_review_timestamp=datetime.datetime.now()
            current_profile.save()
            
            context = {
                
                'current_user' : current_user,
                'current_profile' : current_profile,
                'form': form,
                'reviews_list' : reviews_list,
                'contact' : contact
            }
            return render(request, 'contacts/contact_details/contact_view.html', context)
    context = {
        'current_user' : current_user,
        'form': form,
        'contact': contact,
        'reviews_list' : reviews_list
    }
    return HttpResponse(template.render(context, request))
    
@login_required
def user_profile(request, username):
    current_user = User.objects.get(username=request.user.username)
    name = str(username)
    name = name.replace('/send','')
    name = name.replace("'u",'')
    profile = Profile.objects.get(user=User.objects.get(username=name))
    contacts_list = Contact.objects.filter(created_by=profile.user).order_by('contact_type')
    if Feedback.objects.filter(created_by=profile.user).order_by('-time_stamp').count()>0:
        reviews_list = Feedback.objects.filter(created_by=profile.user).order_by('-time_stamp')[0]
    else:
        reviews_list = "No reviews yet!"
    template = loader.get_template('registration/user_profile.html')
    context = {
        'current_user' : current_user,
        'reviews_list' : reviews_list,
        'last_review' : reviews_list,
        'contacts_list' : contacts_list,
        'profile': profile,
    }
    return HttpResponse(template.render(context, request))