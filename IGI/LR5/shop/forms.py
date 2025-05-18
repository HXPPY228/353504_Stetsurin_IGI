from django import forms
from .models import Order, OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('product','quantity')

OrderItemFormSet = forms.inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=5, can_delete=False
)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ()
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = OrderItemFormSet(self.data or None, instance=self.instance)
