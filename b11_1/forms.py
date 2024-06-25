from django import forms
from django.forms import ModelForm
from .models import Material
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db import connection
from django.urls import reverse_lazy
from django.forms import DateField
from django.conf import settings

#class ServiceForm(ModelForm):
#    service_date = forms.DateField(
#        label='Date du massage ',
#        input_formats=['%d.%m.%Y'],  # Ensures the date accepts this format
#        widget=forms.DateInput(      # Customize the widget as before
#            attrs={
#                'class': 'form-control',
#                'style': 'width:300px;',
#                'placeholder': 'dd.mm.yyyy',  # Changed to a more standard placeholder format
#                'tabindex': 2
#            },  
#            format='%d.%m.%Y'  # Ensure the widget displays dates in this format
#        )   
#    )   
#
#    class Meta:
#        model = Service
#        fields = ['service_client_id', 'service_date', 'service_massage_id', 'service_is_voucher', 'service_cashed_price', 'service_payment_method', 'service_comment', 'service_duration']
#        widgets = { 
#            'service_client_id': forms.Select(attrs={'class':'form-control', 'style':'width: 300px;', 'tabindex':1}),#, 'placeholder':'Nom du client'}),
#            'service_massage_id': forms.Select(attrs={'class':'form-control', 'style':'width: 300px;', 'onchange': "updateMassageInfo();", 'tabindex':3}),#, 'placeholder':'Nom du massage'}),
##            'service_date': forms.DateInput(format="%d.%m.%Y", attrs={'class':'form-control', 'style':'width:300px;', 'placeholder':'jj.mm.aaaa', 'tabindex':2}),
#            'service_comment': forms.Textarea(attrs={'class':'form-control', 'rows':5}),
#            'service_cashed_price': forms.NumberInput(attrs={'class':'form-control', 'style':'width: 300px;', 'tabindex':5}),#, 'placeholder':'Prix encaissé'}),
#            'service_is_voucher': forms.CheckboxInput(attrs={'class': 'form-check-input', 'tabindex':4}),
#            'service_duration': forms.HiddenInput(),
#            'service_payment_method':forms.Select(choices=Service.PAYMENT_METHOD_CHOICES, attrs={'class':'form-control', 'style':'width:300px'}),
#            'service_comment': forms.Textarea(attrs={'class':'form-control', 'rows':5, 'style':'width: 300px;'})
#         } 

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['positions_nr', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung']
