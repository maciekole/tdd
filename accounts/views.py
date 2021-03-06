from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.urls import reverse
from accounts.models import Token
import sys


# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )

    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for App',
        message_body,
        'noreply@superlists',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    auth.login(request, user)
    return redirect('/')
