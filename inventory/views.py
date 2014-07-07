from django.shortcuts import render
from django.views import generic

from inventory.models import Part, Bin

class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'latest_part_list'

    def get_queryset(self):
        return Part.objects.order_by('-updated')[:10]

class BinListView(generic.ListView):
    template_name = 'inventory/bin.html'
    context_object_name = 'bin_list'
    paginate_by = 3 

    def get_queryset(self):
        return Bin.objects.all()

class BinDetailView(generic.DetailView):
    model = Bin

class SearchView(generic.ListView):
    template_name = 'inventory/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Part.objects

class PartCreate(generic.CreateView):
    model = Part
    fields = ['number', 'package', 'category', 'bins']

def add_inventory(request, bin_id):
    b = get_object_or_404(Bin, pk=bin_id)
    p = Part(number=request.POST['number'], package=request.POST['package'], category=request.POST['category'])
    p.save()
    b.parts.add(p)

