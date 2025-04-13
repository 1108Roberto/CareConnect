from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"


class Client(models.Model):
    name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=255, unique=True)
    BRANCH_CHOICES = [
        ("Auto", "Auto"),
        ("Home", "Home"),
        ("Life", "Life"),
    ]
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Claim(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    claim_number = models.CharField(max_length=255, unique=True)
    date_of_incident = models.DateField()
    date_reported = models.DateField()
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Processing", "Processing"),
        ("Closed", "Closed"),
        ("Rejected", "Rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
