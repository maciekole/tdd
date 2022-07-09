import smtplib
import uuid
import sys
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from accounts.models import Token

# Create your views here.
def send_login_email(request):
    print('request: ', request)
    print('request.POST: ', request.POST)
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    try:
        send_mail(
            'Your login link for App ;)',
            f'Use this link to log in: \n\n{url}',
            'noreply@superlists',
            [email]
        )
        return render(request, 'accounts/login_email_sent.html')
    except smtplib.SMTPAuthenticationError:
        # @todo handle SMTP authentication error <google, not secure shit>
        return redirect('/')

def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')

def logout(request):
    auth_logout(request)
    return redirect('/')
