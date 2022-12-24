from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Contains username, email, password
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank = True, related_name="bidder")
    bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bid}"

class Listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name="owner")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null= True, blank = True, related_name="bidPrice")
    image = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank = True, related_name="category")
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name= "wishlist")

    def __str__(self):
        return self.title
        
    
class Comment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank = True, related_name="customerComment")
    product = models.ForeignKey(Listings, on_delete=models.CASCADE, null= True, blank = True, related_name="productComment")
    message = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.message} / written by: {self.customer}"