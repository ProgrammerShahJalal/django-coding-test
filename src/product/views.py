from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from .models import Variant
from .forms import VariantForm

class VariantView(ListView):
    model = Variant
    template_name = 'product/variant_list.html'
    context_object_name = 'variants'

class VariantCreateView(CreateView):
    model = Variant
    form_class = VariantForm
    template_name = 'product/variant_form.html'

    def get_success_url(self):
        return reverse('product:variants')

class VariantEditView(UpdateView):
    model = Variant
    form_class = VariantForm
    template_name = 'product/variant_form.html'

    def get_success_url(self):
        return reverse('product:variants')

    def get_object(self, queryset=None):
        id = self.kwargs['id']
        return get_object_or_404(Variant, id=id)
