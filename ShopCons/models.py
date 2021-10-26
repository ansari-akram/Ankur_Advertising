from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_gst(value):
    if len(str(value)) != 15:
        raise ValidationError(
            _('GST No. should be 15 digits')
        )


def validate_mob(value):
    if len(str(value)) < 10 or len(str(value)) > 15:
        raise ValidationError(
            _('Mobile No. should be between 10 to 15 digits')
        )


def validate_adhaar(value):
    if len(str(value)) != 12:
        raise ValidationError(
            _('Adhaar No. should be 12 digits')
        )


departments = [('General Store', 'General Store'),
               ('Medical Store', 'Medical Store'),
               ('Chicken Shop', 'Chicken Shop'),
               ('Mutton Shop', 'Mutton Shop'),
               ('Cake Shop', 'Cake Shop'),
               ('Bakery', 'Bakery')
               ]


class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/ShopkeeperProfilePic/', null=True, blank=True)
    shpadhaar_pic = models.ImageField(upload_to='profile_pic/ShopkeeperAdhaar/', null=True, blank=True)
    shopname = models.CharField(max_length=200)
    shopaddr = models.CharField(max_length=200)
    shoptype = models.CharField(max_length=200, choices=departments, default='General Store')
    mobilenum = models.IntegerField(validators=[validate_mob], null=True)
    adhaarnum = models.IntegerField(validators=[validate_adhaar], null=True)
    gstnum = models.IntegerField(validators=[validate_gst], null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{}: {} ({})".format(self.user.first_name, self.shopname, self.shoptype)


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/ConsumerProfilePic/', null=True, blank=True)
    conadhaar_pic = models.ImageField(upload_to='profile_pic/ConsumerAdhaar/', null=True, blank=True)
    address = models.CharField(max_length=200)
    mobilenum = models.IntegerField(validators=[validate_mob], null=True)
    adhaarnum = models.IntegerField(validators=[validate_adhaar], null=True)
    assignedShopId = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (Shop ID: " + self.assignedShopId + ")"


class Admit(models.Model):
    shopId = models.PositiveIntegerField(null=True)
    consId = models.PositiveIntegerField(null=True)
    shopName = models.CharField(max_length=200, null=True)
    consName = models.CharField(max_length=200, null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
