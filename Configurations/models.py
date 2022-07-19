from django.db import models

# Create your models here.
from django.db import models,transaction

# Create your models here.
class configurationGroup(models.Model):
    configurationGroupId = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Group name",max_length=255,null=False)
    sortOrder = models.IntegerField(verbose_name="Sort Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class configuration(models.Model):
    configurationId = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Configuration Name",null=False,max_length=255)
    accessKey = models.CharField(verbose_name="Access Key",null=False,max_length=255)
    fieldChoice = (
        ('text','Text'),
        ('boolean','Boolean'),
        ('select','Select'),
        ('mailTemplate','Mail Template'),
    )
    FieldType = models.CharField(verbose_name="Field Type",max_length=50,choices=fieldChoice,default='text',null=False)
    group = models.ForeignKey(configurationGroup,on_delete=models.CASCADE,null=False)
    value = models.CharField(verbose_name="Value",max_length=255,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class configurationValue(models.Model):
    configurationValueId = models.AutoField(primary_key=True)
    key = models.CharField(verbose_name="Key",max_length=255)
    value = models.CharField(verbose_name="Value",max_length=255)
    sortOrder = models.IntegerField(verbose_name="Sort Order")
    isDefault = models.BooleanField(("Is Default"),default=False)
    configurationName = models.ForeignKey(configuration,on_delete=models.CASCADE,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(configurationValue, self).save(*args, **kwargs)
        with transaction.atomic():
            configurationValue.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(configurationValue, self).save(*args, **kwargs)
