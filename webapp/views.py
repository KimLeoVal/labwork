from django.db.models import Q
from django.db.models.functions import Lower
from django.http import QueryDict, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp import forms
from webapp.forms import ProductForm, SearchForm, OrderForm, AddQtyToBasketForm
from webapp.models import Product, CHOICE, ProInBasket, Order, OrderBasket


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
        self.answer_form = self.get_answer_form()
        self.answer_value = self.get_answer_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(
                Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Product.objects.filter(remain__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        context['form2'] = AddQtyToBasketForm()

        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)
    def get_answer_form(self):
        return AddQtyToBasketForm(self.request.GET)
    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")
    def get_answer_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("answer")
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



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddQtyToBasketForm
        return context


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
#         if request.POST.get('Yes')=='????':
#         # if 'Yes' in request.POST:
#             product.delete()
#         return redirect('index_view')

def category_view(request, category):
    print(category)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products': products})


def add_in_basket(request, pk):
    quantity = 0
    product = get_object_or_404(Product, pk=pk)
    if request.method=='GET':

        product = get_object_or_404(Product, pk=pk)
        if product.remain != 0:
            # print(product.remain)
            # product.remain -= 1
            # product.save()
            quantity += 1
            basket = ProInBasket.objects.all()
            if not basket:
                ProInBasket.objects.create(product_id=pk, quantity=quantity)
            else:
                try:
                    prod = get_object_or_404(ProInBasket, product_id=pk)
                    qty = prod.quantity + 1
                    if qty > product.remain:
                        qty = prod.quantity
                        prod.quantity = qty
                        prod.save()
                    else:
                        qty = prod.quantity + 1
                        prod.quantity = qty
                        prod.save()
                except:
                    ProInBasket.objects.create(product_id=pk, quantity=quantity)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        # product = get_object_or_404(Product, pk=pk)
        # print(product)
        if product.remain != 0:
            # print(product.remain)
            quantity = int(request.POST.get('qty'))
            # print(quantity)
            basket = ProInBasket.objects.all()
            # print(basket)
            if not basket:
                if quantity > product.remain :
                    quantity = product.remain
                ProInBasket.objects.create(product_id=pk, quantity=quantity)

            else:
                try:
                    if quantity > product.remain:
                        quantity = product.remain
                    prod = get_object_or_404(ProInBasket,product_id = product.pk)

                    qty = prod.quantity  + quantity


                    if qty > product.remain:
                        qty = product.remain
                        prod.quantity = qty
                        prod.save()
                    else:
                        prod.quantity = qty
                        prod.save()
                except:
                    ProInBasket.objects.create(product_id=pk, quantity=quantity)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['products'] = self.sum_prod()
        context['total'] = self.total()
        context['form'] = OrderForm
        return context



class DeleteFromBasket(DeleteView):
    model = ProInBasket
    template_name = 'delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('Basket')



def delete_one_by_one(request,pk):
    product = get_object_or_404(ProInBasket,pk=pk)
    if product.quantity >1:
        qty = product.quantity -1
        product.quantity = qty
        product.save()
    elif product.quantity ==1:
        product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))




class CreateOrder(CreateView):
    model = Order
    template_name = 'basket.html'
    form_class = OrderForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        products = ProInBasket.objects.all()
        order_id = self.object.pk
        for product in products:
            OrderBasket.objects.create(order_id=order_id, product_id=product.product.pk, quantity=product.quantity)
            pro = get_object_or_404(Product,pk = product.product.pk)
            remain = pro.remain - product.quantity
            pro.remain = remain
            pro.save()

        products.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('IndexView')


# def createorder(request):
#     if request.method == "GET":
#         form = OrderForm()
#         return render(request, 'basket.html', {'form': form})
#     else:
#         form = OrderForm(data=request.POST)
#     if form.is_valid():
#         order = form.save()
#         products = ProInBasket.objects.all()
#         order_id = order.pk
#         for product in products:
#             OrderBasket.objects.create(order_id=order_id, product_id=product.product.pk, quantity=product.quantity)
#         return redirect('Basket')
#     return render(request, 'basket.html', {"form": form})
