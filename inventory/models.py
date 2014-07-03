from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

def get_sentinel_category():
    return Category.objects.get_or_create(name='DEFAULT')[0]

class Package(models.Model):
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

def get_sentinel_package():
    return Package.objects.get_or_create(name='DEFAULT')[0]

class Part(models.Model):
    number = models.CharField(max_length=256)
    description = models.TextField()
    package = models.ForeignKey('Package', related_name='parts', on_delete=models.SET(get_sentinel_package))
    category = models.ForeignKey('Category', related_name='parts', on_delete=models.SET(get_sentinel_category))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.number

def get_sentinel_part():
    return Part.objects.get_or_create(number='DEFAULT')[0]

class Bin(models.Model):
    FULL = 'full'
    HALF_FULL = 'half'
    EMPTY = 'empty'
                
    QUANTITY_CHOICES = (
            (FULL, 'Full'),
            (HALF_FULL, 'Half full'),
            (EMPTY, 'Empty'),
    )  
    
    number = models.CharField(max_length=64)
    description = models.TextField()
    quantity = models.CharField(max_length=32, choices=QUANTITY_CHOICES, default=EMPTY)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    part = models.ForeignKey('Part', related_name='bins', on_delete=models.SET(get_sentinel_part))

    def __unicode__(self):
        return self.number
