from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from product.models import Variant, Product, ProductVariant
from product.forms import ProductForm, ProductVariantFormSet
from django.views.generic import ListView
from django.db import transaction

class CreateProductView(View):
    template_name = 'products/create.html'

    def get(self, request, *args, **kwargs):
        product_form = ProductForm()
        variant_formset = ProductVariantFormSet()
        variants = Variant.objects.filter(active=True).values('id', 'title')
        return render(request, self.template_name, {'product_form': product_form, 'variant_formset': variant_formset, 'variants': list(variants)})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        product_form = ProductForm(request.POST)
        variant_formset = ProductVariantFormSet(request.POST, prefix='variants')

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            
            for form in variant_formset:
                if form.cleaned_data:
                    variant_title = form.cleaned_data['variant']
                    variant, created = Variant.objects.get_or_create(title=variant_title)

                    product_variant = ProductVariant(
                        product=product,
                        variant=variant,
                        price=form.cleaned_data['price'],
                        stock=form.cleaned_data['stock']
                    )
                    product_variant.save()
            
            return redirect('product:list.product')
        else:
            print(product_form.errors)
            print(variant_formset.errors)
            
            variants = Variant.objects.filter(active=True).values('id', 'title')
            return render(request, self.template_name, {'product_form': product_form, 'variant_formset': variant_formset, 'variants': list(variants)})

class ProductListView(View):
    template_name = 'products/list.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()

        paginator = Paginator(product_list, self.paginate_by)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'products': products})

    def get_queryset(self):
        return Product.objects.all()
