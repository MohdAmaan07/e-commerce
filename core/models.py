from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_PLATINUM = 'P'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_PLATINUM, 'Platinum'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    phone = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
class Order(models.Model):
    PAYEMENT_STATUS_PENDING = 'P'
    PAYEMENT_STATUS_COMPLETED = 'C'
    PAYEMENT_STATUS_FAILED = 'F'
    PAYEMENT_STATUS_CHOICES = [
        (PAYEMENT_STATUS_PENDING, 'Pending'),
        (PAYEMENT_STATUS_COMPLETED, 'Completed'),
        (PAYEMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYEMENT_STATUS_CHOICES, default=PAYEMENT_STATUS_PENDING)
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    