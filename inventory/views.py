import csv
import StringIO

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

from inventory.models import Part, Bin, Package, Category

class IndexView(generic.ListView):
    template_name = 'inventory/index.html'
    context_object_name = 'latest_part_list'

    def get_queryset(self):
        return Part.objects.order_by('-updated').filter(status=Part.PRESENT)[:10]

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
    class PartForm(forms.ModelForm):
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

def report_empty(request, pk):
    part = get_object_or_404(Part, pk=pk)
    part.status = Part.EMPTY
    part.save()
    return render(request, 'inventory/report_empty.html', {'part': part})

def search(request):
    results = Part.search_manager.search(request.GET['q']).filter(status=Part.PRESENT)
    return render(request, 'inventory/search.html', {'results': results, 'query': request.GET['q']}) 

def generate_search_views(request):
    for part in Part.objects.all():
        part.update_search_field()
    return HttpResponseRedirect('/') 

def export(request):
    out_buffer = StringIO.StringIO()
    writer = csv.writer(out_buffer)
    for bin_obj in Bin.objects.all():
        for part in bin_obj.parts.all():
            writer.writerow([bin_obj.number, bin_obj.description, bin_obj.quantity, part.number, part.description, part.package.name, part.category.name])
    response = HttpResponse(out_buffer.getvalue(), 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response

def import_view(request):
    class ImportForm(forms.Form):
        file = forms.FileField()
    if request.method == 'GET':
        return render(request, 'inventory/import.html', {'form': ImportForm()})
    elif request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            reader = csv.reader(request.FILES['file'])
            for row in reader:
                bin_obj = Bin.objects.get_or_create(number=row[0])[0]
                bin_obj.description = row[1]
                bin_obj.quantity = row[2]
                bin_obj.save()

                package = Package.objects.get_or_create(name=row[5])[0]
                package.save()

                category = Category.objects.get_or_create(name=row[6])[0]
                category.save()

                part = Part.objects.get_or_create(number=row[3], package=package)[0]
                part.description = row[4]
                
                part.category = category
                part.save()

                bin_obj.parts.add(part)
            return HttpResponseRedirect('/import')
