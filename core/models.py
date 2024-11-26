from django.db import models
from django.contrib.auth.models import User

class Userdetails(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('JK', 'Jammu and Kashmir'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=2,choices=STATE_CHOICES)
    pincode=models.IntegerField(
        default=0,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.id)


class new_arrival(models.Model):
        
        CATEGORY_CHOICES = [
        ('NEWARRIVAL','newarrival'),
        ('SHIRTS','shirts'),
        ('T_SHIRTS','t-shirts'),
        ('SWEATSHIRTS','sweatshirts'),
        ('TROUSERS','trousers'),
        ('SHORTS','shorts'),
        ('TRENDING','trending')
    ]
        

        SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
        name=models.CharField(max_length=100)
        category = models.CharField(max_length=30,choices=CATEGORY_CHOICES)
        short_d = models.CharField(max_length=400)
        desc = models.TextField()
        original_price=models.IntegerField(default=1000)
        discounted_price=models.IntegerField()
        size = models.CharField(max_length=2, choices=SIZE_CHOICES,default='S')
        upperwear_img = models.ImageField(upload_to='new_arrival_img')

        def __str__(self):
            return str(self.name)
        


class CartUpperwear(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product=models.ForeignKey(new_arrival, on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=1)



     def __str__(self):
        return str(self.id)
     
     @property
     def price_and_quantity_total(self):
        return self.product.discounted_price*self.quantity

     

class Order(models.Model):
        STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
        
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        customer=models.ForeignKey(Userdetails,on_delete=models.CASCADE)
        cloth=models.ForeignKey(new_arrival,on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=1)
        order_at = models.DateTimeField(auto_now_add=True)
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

        def __str__(self):
             return str(self.id)
