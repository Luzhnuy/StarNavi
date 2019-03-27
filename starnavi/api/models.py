from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user=models.ForeignKey(User,on_delete="CASCADE")
    title=models.CharField(max_length=300)
    body=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
