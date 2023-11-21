from django.forms import forms, ModelForm, CharField, TextInput, Textarea, BooleanField, CheckboxInput, formset_factory, ModelChoiceField
from django import forms
from product.models import Variant, Product

class ProductVariantForm(forms.Form):
    variant = forms.ModelChoiceField(queryset=Variant.objects.all())
    price = forms.FloatField()
    stock = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ProductVariantForm, self).__init__(*args, **kwargs)
        self.fields['price'].initial = 0
        self.fields['stock'].initial = 0

ProductVariantFormSet = formset_factory(ProductVariantForm, extra=1)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description']

    # Additional fields from ProductVariantForm
    variant = forms.ModelChoiceField(queryset=Variant.objects.all(), required=False)
    price = forms.FloatField(initial=0)
    stock = forms.IntegerField(initial=0)
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # You can customize the fields here, e.g., add placeholders
        self.fields['price'].widget.attrs['placeholder'] = 'Enter price'
        self.fields['stock'].widget.attrs['placeholder'] = 'Enter stock'

        
class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }
    