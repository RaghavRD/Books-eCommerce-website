from django.db import models
from AdminApp.models import UserInfo, Product
from datetime import datetime

# Create your models here.
class MyCart(models.Model):
    user = models.ForeignKey(to="AdminApp.UserInfo", on_delete= models.CASCADE)
    book = models.ForeignKey(to="AdminApp.Product", on_delete= models.CASCADE)
    qty = models.IntegerField()
    class Meta:
        db_table = "MyCart"

class OrderMaster(models.Model):
    user = models.ForeignKey(to="AdminApp.UserInfo", on_delete= models.CASCADE)
    amount = models.FloatField(default=7)
    dateOfOrder = models.DateTimeField(default=datetime.now)
    details = models.CharField(max_length=300)
    class Meta:
        db_table = "OrderMaster"
