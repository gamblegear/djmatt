'''
Created on Jul 6, 2013

@author: johnny
'''

from django.contrib.auth.models import User
from models import UserProfile 

def create_user(uid, username, password='123'):
    user = User()
    user.set_password(password)
    user.username = username
    user.save()
    userProfile = UserProfile()
    userProfile.name = uid
    userProfile.is_admin = False
    userProfile.user = user
    userProfile.save()
    
def cost(tmp):
    return tmp