from django.contrib.auth import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin

from django.urls import reverse


import uuid


# Create your models here.



class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)


    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('movieapp:movies_by_category',args=[str(self.slug)])

    def __str__(self):
        return '{}'.format(self.name)


class Movie(models.Model):
    name=models.CharField(max_length=250)
    slug = models.SlugField( unique=True,default=uuid.uuid1)
    desc=models.TextField()
    date=models.DateField()
    actors=models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    trailer=models.URLField( max_length=128,db_index=True,unique=True,blank=True)
    img=models.ImageField(upload_to='pics')
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')

    def get_url(self):
        return reverse('movieapp:movcatdetail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name + ' | ' + str(self.owner)



    class Meta:
        ordering = ('name',)
        verbose_name = 'movies'
        verbose_name_plural = 'movies'




class PetOwner(AbstractBaseUser):
    username = models.TextField(max_length=40)
    first_name = models.CharField(max_length=50, help_text="Enter owner's first name")
    last_name = models.CharField(max_length=50, help_text="Enter owner's last name")
    email = models.EmailField(max_length=50, blank=True, unique=True, help_text="Enter owner's email")
    password = models.CharField(max_length=15, blank=True, unique=True,)

    is_active = models.BooleanField(default=True)

    class Meta:
        """Controls default ordering of records when querying the Model type."""

        ordering = ["first_name", "last_name"]

    def __str__(self):
        """String for representing the Model object."""
        return self.first_name

    def get_absolute_url(self):
        """Returns the url to access a detail record of this pet owner."""
        return reverse("petowner_detail", args=[str(self.id)])

