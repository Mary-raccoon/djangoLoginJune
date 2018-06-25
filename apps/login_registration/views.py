from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.contrib.messages import error

def index(request):
    return render(request, 'log_reg/index.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/')
    user = User.objects.get(email = request.POST['email1'])
    if(bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
        print("password match")
        request.session['first_name']=user.first_name
        request.session['id']=user.id
        messages.success(request, "You successfully loged in")
        return redirect('/wall')
    else:
        print("wrong password")
        return redirect('/')
    print(user.first_name)
   
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, msg in errors.items():
            messages.error(request, msg, extra_tags=field)
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
        
        return redirect('/wall')

def success(request):
    return render(request, 'log_reg/success.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def wall(request):
    print("%%%%%%%%%")
    all_messages = Message.objects.all()
    all_comments = Comment.objects.all()
    print("*************************************")
    print("Wall_msg", all_messages)
    print("Wall_cmt", all_comments)
    return render(request, 'log_reg/wall.html',{"all_messages": all_messages,"all_comments": all_comments} )

def post_message(request):
    print("Post_message")
    m1=Message.objects.create(message=request.POST['message'], author_id = request.session['id'])
    # print(m1.message)
    return redirect('/wall')

def post_comment(request):
    print("Post_comment")
    # this_msg = Comment.message.message_id
    Comment.objects.create(comment=request.POST['comment'], owner_id = request.session['id'], message_id = request.POST['msg_cmt'])
    # print(m1.message)
    return redirect('/wall')