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

class MaterialForm_SMDA(ModelForm):

    werk_1 = forms.ModelChoiceField(queryset=Werk_1.objects.all(), required=True)
    werk_2 = forms.ModelChoiceField(queryset=Werk_2.objects.all(), required=False)
    werk_3 = forms.ModelChoiceField(queryset=Werk_3.objects.all(), required=False)
    werk_4 = forms.ModelChoiceField(queryset=Werk_4.objects.all(), required=False)
    allgemeine_positionstypengruppe = forms.ModelChoiceField(queryset=AllgemeinePositionstypengruppe.objects.all(), required=True)
    vertriebsweg = forms.ModelChoiceField(queryset=Vertriebsweg.objects.all(), required=True)
    fuehrendes_material = forms.CharField(required=False)
    auszeichnungsfeld = forms.ModelChoiceField(queryset=Auszeichnungsfeld.objects.all(), required=False)
    cpv_code = forms.CharField(required=False)
    spare_part_class_code = forms.ModelChoiceField(queryset=SparePartClassCode.objects.all(), required=True)
    fertigungssteuerer = forms.ModelChoiceField(queryset=Fertigungssteuerer.objects.all(), required=True)
    kennzeichen_komplexes_system = CustomBooleanChoiceField(required=False)
    sonderablauf = forms.ModelChoiceField(queryset=Sonderablauf.objects.all(), required=False)
    temperaturbedingung = forms.ModelChoiceField(queryset=Temperaturbedingung.objects.all(), required=False)
    bewertungsklasse = forms.ModelChoiceField(queryset=Bewertungsklasse.objects.all(), required=True)
    systemmanager = forms.CharField(required=False)
    kennziffer_bamf = forms.CharField(required=False)
    mietrelevanz = CustomBooleanChoiceField(required=False)
    next_higher_assembly = forms.CharField(required=False)
    nachschubklasse = forms.CharField(required=False)
    verteilung_apm_kerda = CustomBooleanChoiceField(required=False)
    verteilung_svsaa = CustomBooleanChoiceField(required=False)
    verteilung_cheops = CustomBooleanChoiceField(required=False)
    zuteilung = forms.ModelChoiceField(queryset=Zuteilung.objects.all(), required=True)
    auspraegung = forms.ModelChoiceField(queryset=Auspraegung.objects.all(), required=True)

    class Meta:
        model = Material
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'materialzustandsverwaltung', 'rueckfuehrungscode', 'serialnummerprofil', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werk_1', 'werk_2', 'werk_3', 'werk_4', 'allgemeine_positionstypengruppe', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'cpv_code', 'spare_part_class_code', 'fertigungssteuerer', 'cpv_code', 'kennzeichen_komplexes_system', 'sonderablauf', 'cpv_code', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
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
'waehrung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'preiseinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'lagerfaehigkeit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'exportkontrollauflage':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'cage_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_name':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_adresse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_plz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_ort':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'bemerkung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
# --- END Input_Lieferant
# --- BEGIN GD
'begru':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'materialart_grunddaten':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'sparte':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'produkthierarchie':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'materialzustandsverwaltung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'rueckfuehrungscode':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'serialnummerprofil':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'spare_part_class_code':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_nr_gp':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'warengruppe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'uebersetzungsstatus':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
'endbevorratet':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision_fremd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision_eigen':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'zertifiziert_fuer_flug':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'a_nummer':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_an_psd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_an_ruag':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
# --- END GD
        }
