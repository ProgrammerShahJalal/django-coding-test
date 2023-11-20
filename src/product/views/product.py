from itertools import count
from django.views import generic
from django.shortcuts import render,redirect
from django.core.paginator import Paginator

from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


def ListProductView(request):
    products=Product.objects.all()
    number=products.count()
    pgnator=Paginator(products,2)
    page=request.GET.get("page")
    structed_data=pgnator.get_page(page)

    #get values url
    get_title = request.GET.get('title','')
    get_variant = request.GET.get('variant', '')
    get_price_from = request.GET.get('price_from', '')
    get_price_to = request.GET.get('price_to', '')

    
    if get_title != "" or get_variant != "" or get_price_from != "" or get_price_to != "":
        filtered=products.filter(title__contains=get_title)
        filtered=list(filtered)
        v=None
        if get_variant != "":    
            try:
                v=Variant.objects.get(title=get_variant)
            
                v=list(v.productvariant_set.all())
                for i in v:
                    filtered.append(i.product)
            except:
                pass
        
        price_from=get_price_from
        price_to=get_price_to

        if price_from!="" and price_to!="":
            try:
                price_from=float(price_from)
                price_to=float(price_to)
                p=ProductVariantPrice.objects.filter(price__range=(price_from,price_to))
                for i in p:
                    filtered.append(i.product)
            except:
                pass
                    
        try:
            date=request.GET.get('date')
            d=products.filter(date_created=date)
            filtered=filtered+list(d)
        except:
            pass
        filtered=set(filtered)
        filtered=list(filtered)
        pgnator=Paginator(filtered,2)
        structed_data=pgnator.get_page(page)
        url=request.get_full_path()
        context={
        'structed_data':structed_data,
        'number':number,
        'variants':ProductVariant.objects.all(),
        }
        
    context={
        'structed_data':structed_data,
        'number':number,
        'variants':ProductVariant.objects.all(),
    }
    return render(request,'products/list.html',context)