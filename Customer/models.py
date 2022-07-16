from pyexpat import model
from django.db import models,transaction
from django.forms import ValidationError

# Create your models here.
class customerGroup(models.Model):
    customerGroupId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120,verbose_name="Group Name",unique=True,null=False)
    isDefault = models.BooleanField(verbose_name="Default",default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(customerGroup, self).save(*args, **kwargs)
        with transaction.atomic():
            customerGroup.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(customerGroup, self).save(*args, **kwargs)
def validate_not_spaces(value):
    if isinstance(value, str) and value.strip() == '':
        raise ValidationError(u"You must provide more than just whitespace.")

class customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    firstName = models.CharField(verbose_name="First Name",max_length=255,null=False,unique=True)
    lastName = models.CharField(verbose_name="Last Name",max_length=255,null=False)
    image = models.ImageField(verbose_name="Profile Image",upload_to='images/')
    email = models.EmailField(verbose_name="Email Id",max_length=255,null=False)
    contactNo = models.CharField(verbose_name="Contact",unique=True,max_length=12,null=False)
    password = models.CharField(verbose_name="Password",max_length=255,null=False,blank=False,
                           validators=[validate_not_spaces])
    emailVerified = models.BooleanField(verbose_name="Email Verifiy",default=False)
    emailVerifiedDate = models.CharField(verbose_name="Email Verified Date",max_length=255,blank=True,null=True)
    group = models.ForeignKey('customerGroup',verbose_name="Group Name",on_delete=models.SET_NULL,null=True)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    code = models.CharField(max_length=10,default=0)
    expireDate = models.DateTimeField (null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.firstName)

class address(models.Model):
    addressId = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Adrees Type",max_length=255,null=False)
    streetAddress = models.CharField(verbose_name="Street Name",max_length=255)
    houseNo = models.CharField(verbose_name="House No",max_length=255)
    postalCode = models.CharField(verbose_name="Postal Code",max_length=255)
    landmark = models.CharField(verbose_name="Landmark Address",max_length=255)
    isDefault = models.BooleanField(("Is Default"),default=False)
    customerName = models.ForeignKey(customer,on_delete=models.CASCADE,verbose_name="Customer Name",null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)  

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(address, self).save(*args, **kwargs)
        with transaction.atomic():
            address.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(address, self).save(*args, **kwargs)

