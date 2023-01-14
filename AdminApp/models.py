from django.db import models

# Create your models here.
class Category(models.Model):
    Category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.Category_name

    class Meta:
        db_table = "Category"

class Product(models.Model):
    pname = models.CharField(max_length=70)
    p_short_name = models.CharField(max_length=30)
    author = models.CharField(max_length=60)
    price = models.FloatField(default=200)
    description = models.CharField(max_length=500)
    size = models.FloatField(default=1)
    quantity = models.IntegerField()
    image = models.ImageField(default="abc.jpg", upload_to="images")
    cat = models.ForeignKey(to="Category", on_delete= models.CASCADE)
    class Meta:
        db_table = "Product"

class UserInfo(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    emai = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
    class Meta:
        db_table = "UserInfo"

class PaymentMaster(models.Model):
    cardno = models.CharField(max_length=20)
    cvv = models.CharField(max_length=4)
    expiry = models.CharField(max_length=20)
    balance = models.FloatField(default=50000)
    class Meta:
        db_table = "PaymentMaster"


