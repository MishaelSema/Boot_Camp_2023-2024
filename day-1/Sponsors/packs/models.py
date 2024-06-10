from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pack(models.Model):
    name = models.CharField(max_length=100)
    amount_per_month = models.CharField(max_length=100)
    description = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('TPE', 'Très Petite Entreprise'),
        ('PMI', 'Petite et Moyenne Industrie'),
        ('PME', 'Petite et Moyenne Entreprise'),
        ('SU', 'StartUp'),
        ('autres', 'Autres'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    company_name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=10, choices=COMPANY_TYPE_CHOICES)
    creation_date = models.DateField()
    items = models.ManyToManyField(Item, blank=True)
    amount_per_month = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the instance is new

        if is_new:
            super().save(*args, **kwargs)  # Save the instance to generate a primary key

            if self.pack:
                self.items.set(self.pack.description.all())
                self.amount_per_month = self.pack.amount_per_month
            else:
                self.amount_per_month = self.calculate_price()

            super().save(update_fields=['amount_per_month'])  # Save the updated amount_per_month

            self.send_subscription_email()  # Send the email after saving the amount_per_month
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        if self.pack:
            return f"{self.first_name} - {self.pack.name}"
        else:
            return f"{self.amount_per_month} - Custom Pack"

    def calculate_price(self):
        num_items = self.items.count()
        if 4 <= num_items <= 8:
            return 25000  # Price for 4-8 items
        elif num_items > 8:
            return 80000  # Price for more than 8 items
        else:
            return None  # Invalid number of items, price not available

    def send_subscription_email(self):
        subject = 'New Subscription'
        pack_name = self.pack.name if self.pack else 'Custom Pack'
        items_list = ', '.join([item.name for item in self.items.all()])
        message = f"""
        New subscription details:

        Name: {self.first_name} {self.last_name}
        Email: {self.email}
        Phone: {self.phone_number}
        Address: {self.address}
        Pack: {pack_name}
        Amount per month: {self.amount_per_month}
        Items: {items_list}
        """
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
