from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # user object --> user.notes -- get all notes related to user
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notes")
    
    
    def __str__(self):
        return self.title