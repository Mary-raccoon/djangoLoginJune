from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name'])< 3:
            errors['first_name'] = "First name should be at least 2 characters"
        elif not 'first_name' in errors and not re.match(NAME_REGEX, postData['first_name']):
            errors['first_name'] = "First name must only contain letters"
        if len(postData['last_name'])< 3:
            errors['last_name'] = "Last name should be at least 2 characters"
        elif not 'last_name' in errors and not re.match(NAME_REGEX, postData['last_name']):
            errors['last_name'] = "Last name must only contain letters"
        if not 'email' in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        if len(postData['password'])< 8:
            errors['password'] = "Password should be no fewer than 8 characters in length"
        if len(postData['conf_password'])< 1:
            errors['conf_password'] = "Password conformation can't be blank"
        elif postData['conf_password'] != postData['password']:
            errors['conf_password'] = "Passwords do not match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['email1']) < 1:
            errors['email1'] = "Not a valid email"
        if len(User.objects.filter(email=postData['email1'])) == 0:
            errors['email1'] = "Email does not exist. Register first!"
        if len(User.objects.filter(email=postData['email1'])) == 1:
            password_hash = User.objects.get(email=postData['email1']).password
            if bcrypt.checkpw(postData['password1'].encode(), password_hash.encode()) == False:  
                errors['password1'] = "Incorrect password. Try again!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User_object: {} {} {}>".format(self.first_name, self.last_name, self.email)

class Message(models.Model):
    message = models.TextField(blank=False)
    author = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return "<Message_object: {} {} >".format(self.author, self.message)

class Comment(models.Model):
    comment = models.TextField(blank=False)
    owner = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="posted_cmt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<Comment_object: {} {} >".format(self.owner, self.comment)