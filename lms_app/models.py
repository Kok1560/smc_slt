from django.db import models
from datetime import date
# django.utils.timezone.now
from django.utils import timezone
# Create your models here.

class Inventory(models.Model):
    image = models.ImageField(upload_to='photos/%y/%m/%d', null=True, blank=True)
    product_name = models.CharField(max_length=50, unique=True)
    real_quantity = models.IntegerField(default=0)
    inventory_quantity = models.IntegerField()

    def __str__(self):
        return self.product_name

class Package(models.Model):
    pack_name = models.CharField(max_length=100)

    def __str__(self):
        return self.pack_name

class Product(models.Model):
    categories = [
        ('Dynamic Microphones', 'Dynamic Microphones'),
        ('Condencer', 'Condencer'),
        ('Wireless Kit', 'Wireless Kit'),
        ('Power Cable', 'Power Cable'),
        ('Electric Cable', 'Electric Cable'),
        ('A 56 D', 'A 56 D'),
        ('Signal Cables', 'Signal Cables'),
        ('Drum Kit', 'Drum Kit'),
        ('Accessories', 'Accessories'),
        ('Tools', 'Tools'),
        ('speaker', 'speaker'),
        ('mixer', 'mixer'),
        ('speaker', 'speaker'),
        ('stands', 'stands'),
        ('Equipment', 'Equipment'),
        ('Par light', 'Par light'),
        ('Dimmer Packs', 'Dimmer Packs'),


    ]
    image = models.ImageField(upload_to='photos/%y/%m/%d', null=True, blank=True)
    product_id = models.CharField(max_length=100, unique=True)
    product_name = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    category = models.CharField(max_length=50, choices=categories)
    amount_of_parties = models.IntegerField(default=0)
    pack_name = models.ForeignKey(Package, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.product_id

class Party(models.Model):
    party_code = models.AutoField(primary_key=True)
    party_name = models.CharField(max_length=100)
    leader_name = models.CharField(max_length=100)
    wh_leader = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return str(self.party_code)

class Order(models.Model):
    choices = [
        ('add', 'add'),
        ('recovery', 'recovery'),
    ]
    party_code = models.ForeignKey(Party, on_delete=models.PROTECT)
    product_id = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=choices, default='add')

    def __str__(self):
        return f"{self.product_id} {str(self.party_code)}"

class Maintenance(models.Model):
    product_id = models.CharField(max_length=100)

    def __str__(self):
        return self.product_id


