from django import forms
from django.forms import ModelForm
from .models import Material
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.db import connection
from django.urls import reverse_lazy
from django.forms import DateField
from django.conf import settings
from .models import Basismengeneinheit

def readonly_field_style():
    styles_string = ' '
    
    # List of what you want to add to style the field
    styles_list = [
         'background-color : #d1d1d1;',
    ]
    
    # Converting the list to a string 
    styles_string = styles_string.join(styles_list)
    # or
    # styles_string = ' '.join(styles_list)
    return styles_string

class CustomBooleanChoiceField(forms.TypedChoiceField):
    BOOLEAN_CHOICES = (
        (None, '---'),
        (True, 'Yes'),
        (False, 'No'),
    )

    def __init__(self, required=False, default=None, *args, **kwargs):
        kwargs['initial'] = default
        super().__init__(
            choices=self.BOOLEAN_CHOICES,
            coerce=lambda x: x == 'True',
            required=required,
            empty_value=None,
            *args,
            **kwargs
        )

    def validate(self, value):
        if self.required and (value in self.empty_values or value is None):
            raise forms.ValidationError(self.error_messages['required'], code='required')
        super().validate(value)

class MaterialForm_IL(ModelForm):

    BOOLEAN_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )

    positions_nr = forms.IntegerField(required=True)
    kurztext_de = forms.CharField(required=True)
    kurztext_fr = forms.CharField(required=True)
    kurztext_en = forms.CharField(required=True)
    grunddatentext_de_1_zeile = forms.CharField(required=True)
    grunddatentext_fr_1_zeile = forms.CharField(required=True)
    grunddatentext_en_1_zeile = forms.CharField(required=True)
    basismengeneinheit = forms.ModelChoiceField(queryset=Basismengeneinheit.objects.all(), required=True)
    bruttogewicht = forms.IntegerField(required=True)
    herstellerteilenummer = forms.CharField(required=True)
    instandsetzbar = CustomBooleanChoiceField(required=True)
    chargenpflicht = CustomBooleanChoiceField(required=True)
    lieferzeit = forms.IntegerField(required=True)
    einheit_l_b_h = forms.CharField(required=True)
    laenge = forms.CharField(required=True)
    breite = forms.CharField(required=True)
    hoehe = forms.CharField(required=True)
    preis = forms.CharField(required=True)
    preiseinheit = forms.CharField(required=True)
    hersteller_name = forms.CharField(required=True)
    hersteller_adresse = forms.CharField(required=True)
    hersteller_plz = forms.CharField(required=True)
    hersteller_ort = forms.CharField(required=True)

    class Meta:
        model = Material
        fields = ['positions_nr', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung']
        widgets = {
#'positions_nr'
#'kurztext_de'
#'kurztext_fr'
#'kurztext_en'
#'grunddatentext_de_1_zeile'
#'grunddatentext_de_2_zeile'
#'grunddatentext_fr_1_zeile'
#'grunddatentext_fr_2_zeile'
#'grunddatentext_en_1_zeile'
#'grunddatentext_en_2_zeile'
#'basismengeneinheit'
#'bruttogewicht'
#'gewichtseinheit'
#'nettogewicht'
#'groesse_abmessung'
#'ean_upc_code'
#'nato_stock_number'
#'nsn_gruppe_klasse'
#'nato_versorgungs_nr'
#'herstellerteilenummer'
#'normbezeichnung'
#'gefahrgutkennzeichen'
#'instandsetzbar'
#'chargenpflicht'
#'bestellmengeneinheit'
#'mindestbestellmenge'
#'lieferzeit'
#'einheit_l_b_h'
#'laenge'
#'breite'
#'hoehe'
#'preis'
#'waehrung'
#'preiseinheit'
#'lagerfaehigkeit'
#'exportkontrollauflage'
#'cage_code'
#'hersteller_name'
#'hersteller_adresse'
#'hersteller_plz'
#'hersteller_ort'
#'revision'
#'bemerkung'
            }

class MaterialForm_GD(ModelForm):
    class Meta:
        model = Material
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'materialzustandsverwaltung', 'rueckfuehrungscode', 'serialnummerprofil', 'spare_part_class_code', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werk_1', 'werk_2', 'werk_3', 'werk_4', 'allgemeine_positionstypengruppe', 'verkaufsorg', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'cpv_code', 'fertigungssteuerer', 'cpv_code', 'kennzeichen_komplexes_system', 'sonderablauf', 'cpv_code', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
        widgets = {
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
'basismengeneinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
'gefahrgutkennzeichen':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
#'begru'
#'materialart_grunddaten'
#'sparte'
#'produkthierarchie'
#'materialzustandsverwaltung'
#'rueckfuehrungscode'
#'serialnummerprofil'
#'spare_part_class_code'
#'hersteller_nr_gp'
#'warengruppe'
#'uebersetzungsstatus'
#'endbevorratet'
#'revision_fremd'
#'revision_eigen'
#'zertifiziert_fuer_flug'
#'a_nummer'
#'verteilung_an_psd'
#'verteilung_an_ruag'
'werk_1':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'werk_2':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'werk_3':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'werk_4':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'allgemeine_positionstypengruppe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verkaufsorg':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'vertriebsweg':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'allgemeine_positionstypengruppe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'fuehrendes_material':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'auszeichnungsfeld':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'cpv_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'fertigungssteuerer':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'cpv_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kennzeichen_komplexes_system':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'sonderablauf':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'cpv_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'temperaturbedingung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'bewertungsklasse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'systemmanager':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'kennziffer_bamf':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'mietrelevanz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'next_higher_assembly':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'nachschubklasse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_apm_kerda':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_svsaa':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_cheops':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'zuteilung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'auspraegung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
        }

class MaterialForm_SMDA(ModelForm):
    class Meta:
        model = Material
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'materialzustandsverwaltung', 'rueckfuehrungscode', 'serialnummerprofil', 'spare_part_class_code', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werk_1', 'werk_2', 'werk_3', 'werk_4', 'allgemeine_positionstypengruppe', 'verkaufsorg', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'cpv_code', 'fertigungssteuerer', 'cpv_code', 'kennzeichen_komplexes_system', 'sonderablauf', 'cpv_code', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
        widgets = {
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
'basismengeneinheit':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
'gefahrgutkennzeichen':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
'begru':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'materialart_grunddaten':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'sparte':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'produkthierarchie':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'materialzustandsverwaltung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'rueckfuehrungscode':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'serialnummerprofil':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'spare_part_class_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'hersteller_nr_gp':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'warengruppe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'uebersetzungsstatus':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'endbevorratet':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision_fremd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'revision_eigen':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'zertifiziert_fuer_flug':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'a_nummer':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_an_psd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
'verteilung_an_ruag':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#'werk_1'
#'werk_2'
#'werk_3'
#'werk_4'
#'allgemeine_positionstypengruppe'
#'verkaufsorg'
#'vertriebsweg'
#'allgemeine_positionstypengruppe'
#'fuehrendes_material'
#'auszeichnungsfeld'
#'cpv_code'
#'fertigungssteuerer'
#'cpv_code'
#'kennzeichen_komplexes_system'
#'sonderablauf'
#'cpv_code'
#'temperaturbedingung'
#'bewertungsklasse'
#'systemmanager'
#'kennziffer_bamf'
#'mietrelevanz'
#'next_higher_assembly'
#'nachschubklasse'
#'verteilung_apm_kerda'
#'verteilung_svsaa'
#'verteilung_cheops'
#'zuteilung'
#'auspraegung'
        }
