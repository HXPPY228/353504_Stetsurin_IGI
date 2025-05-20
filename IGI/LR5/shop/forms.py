from django import forms
from .models import Order, OrderItem, Review
from django.core.exceptions import ValidationError

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating','text')
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            return rating
        if rating > 5:
            raise ValidationError('Рейтинг должен быть от 0 до 5.')
        return rating