from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CommaSeparatedIntegerField
from django_countries.fields import CountryField
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name=models.CharField(max_length=255)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(blank=True)
    quantity=models.IntegerField(default=0)
    ali = models.BooleanField(default=False)
    price = models.FloatField()
    def __str__(self):
        return self.name


class Customer(models.Model):
    name=models.CharField(max_length=255)
    phno=models.CharField(max_length=10)
    address=models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    DOB=models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name

class Address(models.Model):
    
    street_address = models.CharField(max_length=100)
    
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
   

    def __str__(self):
        return self.costumer.name

class OrderItem(models.Model):
    
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_final_price(self):
        return self.quantity * self.item.price




class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)                         
    orderid = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    payment = models.BooleanField(default=False)
    

    def __str__(self):
        return self.customer.name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        
        return total






class covid(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    symptoms=models.CharField(max_length=255)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    

class Prescription(models.Model):
    customer = models.ForeignKey(Customer,default=None,on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'prescriptions/')
 
    def __str__(self):
        return self.customer.name


