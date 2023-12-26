from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MaincategoryModel(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='maincategory')

    def __str__(self):
        return self.name

class ProductModel(models.Model):
    mcate = models.ForeignKey(MaincategoryModel,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'photos/product')
    og_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    sell_price = models.IntegerField(default=0)
    description = models.TextField()

    def _str_(self):
            return self.name
    def discounted_price(self):
        return (self.og_price * self.discount)/100
    def selling_price(self):
        return (self.og_price - self.discounted_price())
    
    def save(self, *args, **kwargs):
        self.discount_price = self.discounted_price()
        self.sell_price = self.selling_price()
        super(ProductModel, self).save(*args, **kwargs)


class cartmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,null=True,blank=True) 
    quantity=models.IntegerField(default=1)
   
    def _str_(self):
        return self.product.name

    def prod_total(self):
        return (self.product.sell_price * self.quantity)


class wishlistmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(ProductModel,on_delete=models.CASCADE,null=True,blank=True) 
    quantity=models.IntegerField(default=1)
   

class CustomeraddressModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    counrty = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    add1 = models.CharField(max_length=200)
    add2 = models.CharField(max_length=200)


    def _str_(self):
        return self.fname

step = (('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Shipping','Shipping'),('Deliverd','Deliverd'))

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomeraddressModel,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=step,max_length=200,default='Pending')

    def prod_total(self):
        return (self.product.sell_price * self.quantity)

class contactmodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject= models.TextField(max_length=200)
    message=models.TextField(max_length=500)

    def _str_(self):
        return self.name