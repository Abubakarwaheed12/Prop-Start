from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    BookingCall,
    TakeQuiz,
    PaymentHistory,
    PromoCode,
    FullDiscountPromoCode,
)

admin.site.register(BookingCall)
admin.site.register(TakeQuiz)
admin.site.register(PaymentHistory)
class FullDiscountPromoCodeAdminForm(forms.ModelForm):
    class Meta:
        model = FullDiscountPromoCode
        fields = '__all__'

    def clean_promo_code(self):
        promo_code = self.cleaned_data.get('promo_code')

        if PromoCode.objects.filter(promo_code=promo_code).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This Promo code already exists in Promo Code table.")

        return promo_code

class FullDiscountPromoCodeAdmin(admin.ModelAdmin):
    form = FullDiscountPromoCodeAdminForm

admin.site.register(FullDiscountPromoCode, FullDiscountPromoCodeAdmin)




class PromoCodeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if PromoCode.objects.count() > 0:
            return False 
        return super().has_add_permission(request)

admin.site.register(PromoCode, PromoCodeAdmin)


# class CallAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(is_paid=True)

# admin.site.register(BookingCall, CallAdmin)