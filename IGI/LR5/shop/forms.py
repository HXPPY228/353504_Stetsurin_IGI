from django import forms
from .models import Order, OrderItem, Review
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from datetime import date

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
    
PHONE_REGEX = r'^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$'

class SignUpForm(UserCreationForm):
    phone = forms.RegexField(
        regex=PHONE_REGEX,
        error_messages={'invalid': 'Телефон в формате +375 (29) XXX-XX-XX'},
        label="Телефон"
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'}),
        label="Дата рождения"
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username','first_name','last_name','email','phone','birth_date')

    def clean_birth_date(self):
        bd = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        if age < 18:
            raise ValidationError("Вам должно быть не менее 18 лет.")
        return bd