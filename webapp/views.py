from django.db.models import Q
from django.db.models.functions import Lower
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm, SearchForm
from webapp.models import Product, CHOICE, ProInBasket


class IndexView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 5
    ordering = ['category', 'name']

    # def get_queryset(self):
    #     return Product.objects.filter(remain__gt=0)

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Product.objects.filter(remain__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")
    # if not request.GET:
    #     form = SearchForm()
    #     products = Product.objects.filter(remain__gt=0).order_by(Lower('category'), Lower('name'))
    #     return render(request, 'index.html', {'products': products,'form':form})
    # elif request.GET:
    #     src = request.GET.get('name').capitalize()
    #     print(src)
    #     form = SearchForm()
    #     products = Product.objects.all()
    #     print(products)
    #     products = Product.objects.filter(name=src)
    #     return render(request, 'index.html', {'products': products, 'form': form})




class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
# def product_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'product.html', {'product': product})

class CreateProduct(CreateView):
    model = Product
    template_name = 'create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('ProductView', kwargs={'pk': self.object.pk})

# def create_product(request):
#     if request.method == "GET":
#         form = ProductForm()
#         return render(request, 'create.html', {'form': form})
#     else:
#         form = ProductForm(data=request.POST)
#     if form.is_valid():
#         new_prod = form.save()
#         return redirect('product_view',pk=new_prod.pk)
#     return render(request,'create_product',{"form":form})

class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('ProductView', kwargs={'pk': self.object.pk})
# def update_product(request,pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "GET":
#         form = ProductForm(initial={
#             "name": product.name,
#             "description": product.description,
#             "category": product.category,
#             "remain": product.remain,
#             "price": product.price,
#         })
#         return render(request, 'update.html', {'form': form})
#     else:
#
#         form = ProductForm(data=request.POST)
#
#         if form.is_valid():
#             product.name = form.cleaned_data.get("name")
#             product.description = form.cleaned_data.get("description")
#             product.category = form.cleaned_data.get("category")
#             product.remain = form.cleaned_data.get("remain")
#             product.price = form.cleaned_data.get("price")
#             product.save()
#             return redirect('index_view')
#         return render(request, 'update.html', {"form": form})

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('IndexView')
# def delete_product(request,pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         return render(request, 'delete.html',{'product':product})
#     else:
#         print(request.POST)
#         a = request.POST.get('name')
#         print(a)
#         if request.POST.get('Yes')=='Да':
#         # if 'Yes' in request.POST:
#             product.delete()
#         return redirect('index_view')

def category_view(request,category):
    print(category)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products': products})

def add_in_basket(request,pk):
    quantity = 0
    product = get_object_or_404(Product,pk=pk)
    if product.remain != 0:
        product.remain -=1
        product.save()
        quantity +=1
        basket = ProInBasket.objects.all()
        if not basket:
            ProInBasket.objects.create(product_id=pk, quantity=quantity)
        else:
            try:
                prod = get_object_or_404(ProInBasket, product_id=pk)
                qty = prod.quantity + 1
                prod.quantity = qty
                prod.save()
            except:
                ProInBasket.objects.create(product_id=pk, quantity=quantity)
    return redirect('IndexView')

# def basket(request):
#     total = 0
#     products = ProInBasket.objects.all()
#     for product in products:
#         sum_pro = product.quantity * product.product.price
#         product.sum_pro = sum_pro
#         product.save()
#         total += product.sum_pro
#     return render(request, 'basket.html', {'products': products, 'total':total})

class Basket(ListView):
    model = ProInBasket
    template_name = 'basket.html'
    context_object_name = 'products'
    paginate_by =2

    def sum_prod(self):
        total = 0
        products = ProInBasket.objects.all()
        for product in products:
            sum_pro = product.quantity * product.product.price
            product.sum_pro = sum_pro
            product.save()
            total += product.sum_pro
        return products

    def total(self):
        total = 0
        products = ProInBasket.objects.all()
        for product in products:
            sum_pro = product.quantity * product.product.price
            total += sum_pro
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.sum_prod()
        context['total'] = self.total()
        return context








