from django.db import models

class Post(models.Model):
    '''Post model for the storage of all posts'''
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)