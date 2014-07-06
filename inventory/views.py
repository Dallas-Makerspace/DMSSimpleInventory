from django.shortcuts import render
from django.views import generic

from inventory.models import Part, Bin

class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'latest_part_list'

    def get_queryset(self):
        return Part.objects.order_by('-updated')[:10]

class SearchView(generic.ListView):
    template_name = 'inventory/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Part.objects

class PartCreate(generic.CreateView):
    model = Part
    fields = ['number', 'package', 'category', 'bins']

