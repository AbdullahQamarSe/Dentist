# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


from django.core.mail import send_mail
import random

def generate_verification_code():
    # Generate a random 6-digit verification code
    return str(random.randint(100000, 999999))

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Generate a verification code
            verification_code = generate_verification_code()
            form.cleaned_data['verification_code'] = verification_code

            # Send the verification code to the user's email
            subject = 'Verification Code for Registration'
            message = f'Your verification code is: {verification_code}'
            from_email = 'your_email@example.com'  # Replace with your email
            recipient_list = [form.cleaned_data.get("email")]
            send_mail(subject, message, from_email, recipient_list)

            # Temporarily store the user data and verification code in the session
            request.session['user_data'] = form.cleaned_data

            # Redirect to the verify_registration page
            return redirect('verify_registration')

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


from django.contrib.auth.models import User


from django.contrib.auth import login

def verify_registration(request):
    msg = None
    success = False

    if request.method == "POST":
        entered_code = request.POST.get('verification_code')
        stored_data = request.session.get('user_data')

        if entered_code == stored_data.get('verification_code'):
            # Verification code is correct, create the user and log them in
            user = User.objects.create_user(
                username=stored_data['username'],
                email=stored_data['email'],
                password=stored_data['password1']
            )
            login(request, user)

            msg = 'Registration successful!'
            success = True

            # Clear the session data
            del request.session['user_data']
        else:
            msg = 'Verification code is incorrect.'
    else:
        msg = 'Enter the verification code sent to your email.'

    return render(request, "accounts/verify_registration.html", {"msg": msg, "success": success})



from .forms import ResetPasswordForm
from .forms import verifyForm

def forget(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            verification_code = generate_verification_code()
            form.cleaned_data['verification_code'] = verification_code

            # Send the verification code to the user's email
            subject = 'Verification Code for Registration'
            message = f'Your verification code is: {verification_code}'
            from_email = 'your_email@example.com'  # Replace with your email
            recipient_list = [form.cleaned_data.get("email")]
            send_mail(subject, message, from_email, recipient_list)

            # Temporarily store the user data and verification code in the session
            request.session['email'] = form.cleaned_data['email']
            request.session['verify'] = form.cleaned_data['verification_code']

            return redirect('verify_forget')

    else:
        return render(request, "accounts/forgot.html")  
    
    return render(request, "accounts/forgot.html")




def verify_forget(request):
    if request.method == "POST":

        entered_code = request.POST.get('verification_code')
        code = request.session.get('verify')
        
        print(code)
        print(entered_code)

        if entered_code == code:
            return render(request, "accounts/changepassword.html")
            
    else:
        return render(request, "accounts/forget_verify.html")
    return render(request, "accounts/forget_verify.html")




# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ChangePasswordForm

def change_password(request):
    if request.method == 'POST':

        password  = request.POST.get('password')
        confirm_password1  = request.POST.get('confirm_password')

        new_password = password
        confirm_password = confirm_password1

        if new_password == confirm_password:
            # Assuming you store the user's email in request.session['email']
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('login')  # Redirect to login page after changing the password
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match.')
    else:
        return render(request, 'change_password.html')

    return render(request, 'change_password.html')
