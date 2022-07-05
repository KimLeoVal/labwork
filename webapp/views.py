from django.db.models.functions import Lower
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ProductForm, SearchForm
from webapp.models import Product, CHOICE


def index_view(request):
    if not request.GET:
        form = SearchForm()
        products = Product.objects.filter(remain__gt=0).order_by(Lower('category'), Lower('name'))
        return render(request, 'index.html', {'products': products,'form':form})
    elif request.GET:
        src = request.GET.get('name').capitalize()
        print(src)
        form = SearchForm()
        products = Product.objects.all()
        print(products)
        products = Product.objects.filter(name=src)
        return render(request, 'index.html', {'products': products, 'form': form})





def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def create_product(request):
    if request.method == "GET":
        form = ProductForm()
        return render(request, 'create.html', {'form': form})
    else:
        form = ProductForm(data=request.POST)
    if form.is_valid():
        new_prod = form.save()
        return redirect('product_view',pk=new_prod.pk)
    return render(request,'create_product',{"form":form})


def update_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "remain": product.remain,
            "price": product.price,
        })
        return render(request, 'update.html', {'form': form})
    else:

        form = ProductForm(data=request.POST)

        if form.is_valid():
            product.name = form.cleaned_data.get("name")
            product.description = form.cleaned_data.get("description")
            product.category = form.cleaned_data.get("category")
            product.remain = form.cleaned_data.get("remain")
            product.price = form.cleaned_data.get("price")
            product.save()
            return redirect('index_view')
        return render(request, 'update.html', {"form": form})


def delete_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html',{'product':product})
    else:
        if 'Yes' in request.POST:
            product.delete()
        return redirect('index_view')

