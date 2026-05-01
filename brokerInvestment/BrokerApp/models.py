
from django.db import models
from django.contrib.auth.models import User #AbstractUser

# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    account_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    pin = models.CharField(max_length=300, null=True)
    hide_balance = models.BooleanField(default=False)
    frozen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(upload_to='picture', blank=True, null=True)
    date_birth = models.DateField(verbose_name="date of birth", blank=True, null=True)
    date_joined = models.DateField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    block = models.BooleanField(default=False)
    kyc = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Plan(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    name = models.TextField(blank=True, null=True)
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    duration = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Investment(models.Model):
    investment = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='investment', blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor')
    invested_on = models.DateTimeField(verbose_name='invested time', auto_now=True)
    due_time = models.PositiveIntegerField(default=0, blank=True, null=True)
    due = models.BooleanField(default=False)
    days_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.investor.username 
    
    class Meta:
        indexes = [
            models.Index(fields=['investor', 'due']),
        ]
    
class Trasaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions') 
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    status = models.CharField(max_length=10)
    created_date = models.DateField(verbose_name='transaction date', null=True, blank=True, auto_now=True)
    created_at = models.TimeField(verbose_name='transaction time', null=True, blank=True, auto_now=True)
    transaction_id = models.CharField(max_length=20)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction', null=True, blank=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.amount})"

    class Meta:
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
        ]

class Message(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_receiver')
    body = models.TextField()
    date = models.DateField(verbose_name='sent dte', auto_now=True)
    time = models.TimeField(verbose_name='sent time', auto_now=True)

    def __str__(self):
        return str(self.receiver.username)

class OTPCode(models.Model):
    otp = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_receiver')
    created_at = models.DateTimeField(verbose_name='otp time', auto_now=True)

    def __str__(self):
        return self.otp
    
    class Meta:
        indexes = [
            models.Index(fields=['receiver']),
        ]
    
class Account(models.Model):
    address = models.TextField(null=True, blank=True)
    address_name = models.TextField(null=True, blank=True)
    receiver_name = models.TextField(null=True, blank=True)
    date = models.DateField(verbose_name='sent dte', auto_now=True)

    def __str__(self):
        return self.address_name
    
class UserAccount(models.Model):
    address = models.TextField(null=True, blank=True)
    address_name = models.TextField(null=True, blank=True)
    receiver_name = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    date = models.DateField(verbose_name='sent dte', auto_now=True)
    time = models.TimeField(verbose_name='sent time', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_account', null=True, blank=True)

    def __str__(self):
        return self.address_name
    