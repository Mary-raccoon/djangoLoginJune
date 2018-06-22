from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'log_reg/index.html')

def login(request):
    user = User.objects.get(email = request.POST['email'])
    if(bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
        print("password match")
        request.session['first_name']=user.first_name
        messages.success(request, "User successfully created")
        return redirect('/success')
    else:
        print("wrong password")
        return redirect('/')
    print(user.first_name)
   
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash_password)
        User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'],
            password = hash_password
        )
        messages.success(request, "User successfully created")
        
        return redirect('/success')

def success(request):
    return render(request, 'log_reg/success.html')


