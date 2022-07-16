from django.db import models
from django.db import transaction

# Create your models here.
class language(models.Model):
    locale = models.CharField(primary_key=True,max_length=20)
    title = models.CharField(max_length=50,verbose_name="language Name")
    icon = models.ImageField(upload_to='images/')
    isDefault = models.BooleanField(verbose_name="Is Default",default=False)
    statusChoice = (
        ('enabled','Enabled'),
        ('disabled','Disabled'),
    )
    status = models.CharField(max_length=10,choices=statusChoice,default='enabled')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.locale)  

    def save(self, *args, **kwargs):
        if not self.isDefault:
            return super(language, self).save(*args, **kwargs)
        with transaction.atomic():
            language.objects.filter(
                isDefault=True).update(isDefault=False)
            return super(language, self).save(*args, **kwargs)
