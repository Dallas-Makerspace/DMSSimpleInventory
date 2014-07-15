from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms import ModelForm

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

class PartDetailView(generic.DetailView):
    model = Part 

class SearchView(generic.ListView):
    template_name = 'inventory/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Part.objects

class PartCreate(generic.CreateView):
    model = Part
    fields = ['number', 'package', 'category', 'bins']

def add_inventory(request, pk):
    b = get_object_or_404(Bin, pk=pk)
    class PartForm(ModelForm):
        class Meta:
            model = Part
            fields = ['number', 'package', 'category']
    if request.method == 'GET':
        return render(request, 'inventory/add_part_to_bin.html', {'form': PartForm()}) 
    elif request.method == 'POST':
        try:
            form = PartForm(request.POST)
            p = form.save()
            b.parts.add(p)
            return render(request, 'inventory/add_part_to_bin.html', {'message': 'Part added.', 'form': PartForm()})
        except ValueError:
            return render(request, 'inventory/add_part_to_bin.html', {'form': form})

def search(request):
    results = Part.objects.filter(number__contains=request.GET['q'])
    return render(request, 'inventory/search.html', {'results': results}) 
