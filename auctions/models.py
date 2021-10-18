from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone




class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"





class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    title = models.CharField(max_length=120)
    description = models.TextField()
    start_bid = models.FloatField()
    last_bid = models.ForeignKey("Bid", on_delete=models.CASCADE, related_name="last_bid_for_product", blank=True, null=True) 
    # blank=True, null=True - чтобы при добавлении через админке не требовало вторую цену и коммент 
    bids = models.ManyToManyField("Bid", related_name="bids_for_product", blank=True, null=True)
    closed = models.BooleanField(default=False)
    comment = models.ManyToManyField("Comment", blank=True)
    image = models.ImageField(upload_to="static/media", blank=True) # указіваем пусть загрузки медиа файлов через админку

    def __str__(self):
        return f"{self.title}"   

   
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    bid = models.FloatField(default=0, max_length=7)

    def __str__(self):
        return f"{self.bid}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}, {self.date}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user}'s personal watchlist"
