from django import forms
from django.forms import ModelForm
from .models import Material
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db import connection
from django.urls import reverse_lazy
from django.forms import DateField
from django.conf import settings
from .models import *
from .widgets import ReadOnlyForeignKeyWidget
from .utils import readonly_field_style
from .forms import CustomBooleanChoiceField

class MaterialForm_IL(ModelForm):

    positions_nr = forms.IntegerField(required=True)
    kurztext_de = forms.CharField(required=True)
    kurztext_fr = forms.CharField(required=True)
    kurztext_en = forms.CharField(required=True)
    grunddatentext_de_1_zeile = forms.CharField(required=True)
    grunddatentext_de_2_zeile = forms.CharField(required=False)
    grunddatentext_fr_1_zeile = forms.CharField(required=True)
    grunddatentext_fr_2_zeile = forms.CharField(required=False)
    grunddatentext_en_1_zeile = forms.CharField(required=True)
    grunddatentext_en_2_zeile = forms.CharField(required=False)
    basismengeneinheit = forms.ModelChoiceField(queryset=Basismengeneinheit.objects.all(), required=True)
    bruttogewicht = forms.IntegerField(required=True)
    nettogewicht = forms.IntegerField(required=False)
    groesse_abmessung = forms.IntegerField(required=False)
    ean_upc_code = forms.CharField(required=False)
    nato_stock_number = forms.CharField(required=False)
    nsn_gruppe_klasse = forms.CharField(widget=forms.HiddenInput(), required=False)
    nato_versorgungs_nr = forms.CharField(widget=forms.HiddenInput(), required=False)
    herstellerteilenummer = forms.CharField(required=True)
    normbezeichnung = forms.CharField(required=False)
    gefahrgutkennzeichen = forms.CharField(required=False)
    gefahrgutkennzeichen = forms.ModelChoiceField(queryset=Gefahrgutkennzeichen.objects.all(), required=False)
    instandsetzbar = CustomBooleanChoiceField(required=True)
    chargenpflicht = CustomBooleanChoiceField(required=True)
    bestellmengeneinheit = forms.IntegerField(required=False)
    mindestbestellmenge = forms.IntegerField(required=False)
    lieferzeit = forms.IntegerField(required=True)
    laenge = forms.IntegerField(required=True)
    breite = forms.IntegerField(required=True)
    hoehe = forms.IntegerField(required=True)
    preis = forms.IntegerField(required=True)
    preiseinheit = forms.IntegerField(required=True)
    lagerfaehigkeit = forms.IntegerField(required=True)
    exportkontrollauflage = CustomBooleanChoiceField(required=False)
    cage_code = forms.CharField(required=False)
    hersteller_name = forms.CharField(required=True)
    hersteller_adresse = forms.CharField(required=True)
    hersteller_plz = forms.IntegerField(required=True)
    hersteller_ort = forms.CharField(required=True)
    revision = forms.CharField(required=False)
    bemerkung = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=True)

    class Meta:
        model = Material
        fields = ['positions_nr', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'laenge', 'breite', 'hoehe', 'preis', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung']
        widgets = {
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tooltips = HelpTooltip.objects.all()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                field.help_text = tooltip.content
