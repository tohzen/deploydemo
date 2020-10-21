from django.db import models
import re
from datetime import date

from django.db.models.deletion import CASCADE

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]')
        usernameMatch = User.objects.filter(username=postData['username'])
        if len(postData['name']) < 3:
            errors["namereq"] = "Name needs to be at least 3 characters"
            
        if len(postData['username']) < 5:
            errors["usernamereq"] = "Username is required"
        elif not EMAIL_REGEX.match(postData['username']):           
            errors['usernamepattern'] = "Invalid Username!"
        if len(usernameMatch)>0:
            errors['username'] = "Username is already taken"
            
            
        if len(postData['pw']) <3:
            errors["pwreq"] = "Passwords needs to be at least 8 characters"
            
        if postData['pw'] !=postData['cpw']:
            errors['cpwmatch'] = "Confirm password must match"
            
        return errors
    
    def loginValidator(self, postData ):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]')
        usernameMatch = User.objects.filter(username=postData['username'])
        print(usernameMatch)
        if len(postData['username']) < 5:
            errors["usernamereq"] = "username is required"
        elif not EMAIL_REGEX.match(postData['username']):           
            errors['usernamepattern'] = "Invalid username address!"
        elif len(usernameMatch) == 0:
            errors['nousername']= "username is not registered"
        else:
            if usernameMatch[0].password != postData['pw']:
                errors['pwmatch'] = "Incorrect Password!"
                
        return errors
            
        
            
        
            
            
            
class PlacesManager(models.Manager):
    def CreateValidator(self, postData):
        errors = {}
        today=date.today()
        fromdate=postData['datefrom']
        if len(postData['destination']) ==0:
            errors["desterr"] = "No empty entries"
        if len(postData['plan']) == 0:
            errors["planerr"] = "No empty entries"
        if (postData['datefrom']) <str(today):
            errors["datefromerr"] = "Travel dates should be future-dated"
        elif (postData['dateto']) <str(fromdate):
            errors["datetoerr"] = "Travel Date to should not be before the Travel Date From"
        
        return errors
            
            
        


# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()


class Places(models.Model):
    destination=models.CharField(max_length=255)
    travelstart=models.DateField()
    travelend=models.DateField()
    plan=models.CharField(max_length=255)
    uploader=models.ForeignKey(User, related_name="user_places", on_delete=models.CASCADE)
    others=models.ManyToManyField(User, related_name="others_places")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=PlacesManager()
