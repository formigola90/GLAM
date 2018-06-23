from django import forms
from .models import Nation, Region, Contact, Story, ContactType, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class contacts_filter_form(forms.Form):
	contact_type = forms.ModelChoiceField(ContactType.objects.all(),help_text='This field is required. What kind of contact are you searching?')
	nation = forms.ModelChoiceField(Nation.objects.all())
	region = forms.ModelChoiceField(Region.objects.all(),help_text='This field is required. In witch region are you interested?')
	name = forms.CharField(max_length=100, required=False, help_text='This field is NOT required. If you are searching for a specific contact try to type his exact name here!')
	
	#contacted_before = forms.DateTimeField(required=False)
	#pwd = forms.CharField(max_length=100, required=False)
	
class FilterForm_1(ModelForm):
    
    class Meta:
        model = Contact
        fields = ['contact_type', 'nation']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class AddContactForm(forms.Form):
    name = forms.CharField(max_length=100, help_text='100 characters max.')
    nation = forms.ModelChoiceField(Nation.objects.all(),help_text='100 characters max.')
    region = forms.ModelChoiceField(Region.objects.all().order_by('region'),help_text='This field is required. Choose the Region!')
    contact_type = forms.ModelChoiceField(ContactType.objects.exclude(contact_type = 'Person'),help_text='100 characters max.')
    email = forms.EmailField(help_text='100 characters max.')
    website =  forms.URLField(label='Contact website', max_length=1000, help_text='100 characters max.')
    address = forms.CharField(max_length=200, help_text='100 characters max.')
    phone = forms.CharField(max_length=100, required=False, help_text='100 characters max.')
    
class AddContactForm_1(ModelForm):
    fields_1=['name', 'email', 'contact_type', 'nation']
    fields_2=['name', 'email', 'contact_type', 'nation', 'region', 'addres', 'website', 'phone']
    fields_3=fields_1
    nation='__all__'
        
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact_type', 'nation']
        
class AddContactForm_2(ModelForm):
    
    class Meta:
        model = Contact
        fields = ['nation']
    
class FeedbackForm(ModelForm):
    
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']