from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def inventoryPage(request):
    parts = Part.objects.all()
    return render(request, "inventory.part_list.html", {"parts": parts})

@login_required
def index(request):
    form = MyForm()
    rendered_form = form.render("form_snippet.html")
    context = {"form": rendered_form}
    return render(request, "add.html", context)


@login_required
def create_part(request):
    if request.method == 'POST':
        part_name = request.POST.get('part_name')
        quantity_in_stock = request.POST.get('quantity_in_stock')
        unit_cost = request.POST.get('unit_cost')

        new_part = Part(
            part_name=part_name,
            quantity_in_stock=quantity_in_stock,
            unit_cost=unit_cost
        )
        new_part.save()
        return redirect('PartForm')
    return render(request, 'part/part_form.html')

@login_required
def view_part(request, part_id):
    part = Part.objects.get(pk=part_id)
    return render(request, 'part/view_part.html', {'part':part})


@login_required
def part_request(request):
    if request.method == 'POST':
        part_request = Part.objects.all()
        part_request = request.POST.get('part_request')
        new_request = PartsRequest(
            part_request=part_request
        )
        new_request.save()
        return redirect('PartsRequestForm')
    return render(request, 'part/parts_request_form.html')

@login_required
def add_part(request):
    if request.method == 'POST':
        payload = request.POST
        form = PartForm(payload)
        if form.is_valid():
            form.save()
            return redirect('inventoryPage')
    return render(request, 'part/part_form.html', {'form': PartForm()})

@login_required
def part_details(request, part_id):
    part = Part.objects.get(pk=part_id)
    return render(request, 'part/view_part.html', {'part': part})

@login_required
def part_request_details(request, part_request_id):
    part_request = PartsRequest.objects.get(pk=part_request_id)
    return render(request, 'part/view_part_request.html', {'part_request': part_request})

@login_required
def delete_part_request(request, part_request_id):
    part_request = PartsRequest.objects.get(pk=part_request_id)
    part_request.delete()
    return redirect('inventoryPage')

@login_required
def update_part(request, part_id):
    part = Part.objects.get(pk=part_id)
    if request.method == 'POST':
        part.part_name = request.POST.get('part_name')
        part.quantity_in_stock = request.POST.get('quantity_in_stock')
        part.unit_price = request.POST.get('unit_price')
        part.save()
        return redirect('inventoryPage')
    return render(request, 'part/part_form.html', {'part': part})

@login_required
def delete_part(request, part_id):
    part = Part.objects.get(pk=part_id)
    part.delete()
    return redirect('inventoryPage')   

def tests(request):
    return render(request, 'tests.py', {'tests': tests})