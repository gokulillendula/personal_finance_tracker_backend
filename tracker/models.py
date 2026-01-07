from django.db import models
# Import the correct base class: BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager 
# Note: Remove 'UserManager' from imports

# 1. Use BaseUserManager and define both creation methods
class CustomUserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        # Create user instance using email
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        # Crucially, call the custom create_user method, passing only email
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username=None  # Remove username field
    phonenumber=models.CharField(max_length=15,blank=True)
    balance=models.DecimalField(max_digits=100, decimal_places=2, default=0.00,)
    email=models.EmailField(unique=True,blank=False)
    #username='email'

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} (₹{self.balance})"

class Spent(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='spent')
    tid=models.AutoField(primary_key=True)
    amt=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} has spent {self.amt} on {self.date}"
    
class Earned(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='earned')
    tid=models.AutoField(primary_key=True)
    amt=models.DecimalField(max_digits=20,decimal_places=2)
    category=models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} has earned {self.amt} on {self.date}"
class Investments(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='investments')
    tid=models.AutoField(primary_key=True,unique=True)
    amt=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=50)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} has invested {self.amt} on {self.date}"


    

