from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
Desg = (
    ('team lead','team lead'),
    ('investigation head', 'investigation head'),
    ('member','member'),
)
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    designation =   models.CharField(choices = Desg, max_length = 100 , default = '')
    city =   models.CharField(max_length = 100 , default = '')
    unq = models.IntegerField(default =123)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        userprofile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
