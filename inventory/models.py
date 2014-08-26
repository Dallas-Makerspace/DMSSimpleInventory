from django.db import models
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

def get_sentinel_category():
    return Category.objects.get_or_create(name='DEFAULT')[0]

class Package(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

def get_sentinel_package():
    return Package.objects.get_or_create(name='DEFAULT')[0]

class Part(models.Model):
    number = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    package = models.ForeignKey('Package', related_name='parts')
    category = models.ForeignKey('Category', related_name='parts')
    bins = models.ManyToManyField('Bin', related_name='parts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    search_index = VectorField()

    objects = models.Manager()
    search_manager = SearchManager(fields=('number', 'description'),
                                   config='pg_catalog.english',
                                   search_field='search_index',
                                   auto_update_search_field=True)

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = (("number", "package"),)
        ordering = ['number']

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
    
    number = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    quantity = models.CharField(max_length=32, choices=QUANTITY_CHOICES, default=EMPTY)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ['number']
