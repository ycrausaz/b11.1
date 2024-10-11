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
from .forms import CustomBooleanChoiceField, SplitterReadOnlyReadWriteFields

class MaterialForm_GD(ModelForm, SplitterReadOnlyReadWriteFields):

    begru = forms.ModelChoiceField(queryset=BEGRU.objects.all(), required=True)
    materialart_grunddaten = forms.ModelChoiceField(queryset=Materialart.objects.all(), required=True)
    sparte = forms.ModelChoiceField(queryset=Sparte.objects.all(), required=True)
    produkthierarchie = forms.CharField(required=True)
    rueckfuehrungscode = forms.ModelChoiceField(queryset=Rueckfuehrungscode.objects.all(), required=False)
    serialnummerprofil = forms.ModelChoiceField(queryset=Serialnummerprofil.objects.all(), required=True)
    hersteller_nr_gp = forms.CharField(required=True)
    warengruppe = forms.CharField(required=True)
    uebersetzungsstatus = forms.ModelChoiceField(queryset=Uebersetzungsstatus.objects.all(), required=True)
    endbevorratet = forms.CharField(required=False)
    revision_fremd = forms.CharField(required=False)
    revision_eigen = forms.CharField(required=False)
    zertifiziert_fuer_flug = CustomBooleanChoiceField(required=False)
    a_nummer = forms.CharField(required=False)
    verteilung_an_psd = CustomBooleanChoiceField(required=False)
    verteilung_an_ruag = CustomBooleanChoiceField(required=False)

    class Meta:
        model = Material
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'rueckfuehrungscode', 'serialnummerprofil', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werkzuordnung_1', 'werkzuordnung_2', 'werkzuordnung_3', 'werkzuordnung_4','allgemeine_positionstypengruppe', 'verkaufsorg', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'spare_part_class_code', 'fertigungssteuerer', 'kennzeichen_komplexes_system', 'sonderablauf', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'orderbuchpflicht', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
        widgets = {
# --- BEGIN IL
'positions_nr':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kurztext_de':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kurztext_fr':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kurztext_en':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_de_1_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_de_2_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_fr_1_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_fr_2_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_en_1_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'grunddatentext_en_2_zeile':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'basismengeneinheit':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'bruttogewicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'gewichtseinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nettogewicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'groesse_abmessung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'ean_upc_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nato_stock_number':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nsn_gruppe_klasse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nato_versorgungs_nr':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'herstellerteilenummer':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'normbezeichnung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'gefahrgutkennzeichen':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'bruttogewicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'instandsetzbar':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'chargenpflicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'bestellmengeneinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'mindestbestellmenge':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'lieferzeit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'einheit_l_b_h':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'laenge':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'breite':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hoehe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'preis':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'preiseinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'lagerfaehigkeit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'exportkontrollauflage':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'cage_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_name':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_adresse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_plz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_ort':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'bemerkung': forms.Textarea(attrs={'class':'form-control','rows':5,'readonly':True,'style':readonly_field_style()}),
# --- END IL
# --- BEGIN SMDA
'werkzuordnung_1':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'werkzuordnung_2':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'werkzuordnung_3':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'werkzuordnung_4':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'allgemeine_positionstypengruppe':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'verkaufsorg':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'vertriebsweg':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'allgemeine_positionstypengruppe':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'fuehrendes_material':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'auszeichnungsfeld':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'spare_part_class_code':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'fertigungssteuerer':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'kennzeichen_komplexes_system':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'sonderablauf':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'temperaturbedingung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'bewertungsklasse':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'systemmanager':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kennziffer_bamf':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'mietrelevanz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'next_higher_assembly':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nachschubklasse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'orderbuchpflicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_apm_kerda':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_svsaa':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_cheops':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'zuteilung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'auspraegung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
# --- END SMDA
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tooltips = HelpTooltip.objects.all()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                field.help_text = tooltip.content
