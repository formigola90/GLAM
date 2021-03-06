from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives

from .forms import SignUpForm
from .tokens import account_activation_token, AccountActivationTokenGenerator




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account on www.ColouredSweat.com'
            message = render_to_string('account_activation_email.html', {'user': user,'domain': current_site.domain,'uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': account_activation_token.make_token(user),})
            user.email_user(subject, message)
            return render(request,'activation_email_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        subject, from_email, to = 'Coloured Sweat - NEW USER', 'colouredsweat@gmail.com', 'colouredsweat@gmail.com'
        text_content = 'User '+user.username+' has activated his profile on your web-site'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()
        login(request, user)
        return redirect('contacts:index')
    else:
        return render(request, 'account_activation_invalid.html')