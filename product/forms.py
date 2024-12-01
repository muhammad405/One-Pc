from django import forms
from django.core.exceptions import ValidationError
from .models import ProductTecInfo


class ProductTecInfoForm(forms.ModelForm):
    class Meta:
        model = ProductTecInfo
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tec_info = cleaned_data.get('tec_info')
        tec_info_name = cleaned_data.get('tec_info_name')

        # Validatsiya
        if tec_info_name and tec_info_name.tec_info != tec_info:
            self.add_error('tec_info_name', 'Tanlangan "tec_info_name" tanlangan "tec_info" bilan bog‘liq emas.')

        return cleaned_data