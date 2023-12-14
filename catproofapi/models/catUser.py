from django.db import models
from django.contrib.auth.models import User


class CatUser(models.Model):
    
   
    
    bio = models.TextField(max_length=200)
    # created_on = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cat_user")
