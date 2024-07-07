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
    nsn_gruppe_klasse = forms.CharField(required=False)
    nato_versorgungs_nr = forms.CharField(required=False)
    herstellerteilenummer = forms.CharField(required=True)
    normbezeichnung = forms.CharField(required=False)
    gefahrgutkennzeichen = forms.CharField(required=False)
    gefahrgutkennzeichen = forms.ModelChoiceField(queryset=Gefahrgutkennzeichen.objects.all(), required=False)
    instandsetzbar = CustomBooleanChoiceField(required=True)
    chargenpflicht = CustomBooleanChoiceField(required=True)
    bestellmengeneinheit = forms.IntegerField(required=False)
    mindestbestellmenge = forms.IntegerField(required=False)
    lieferzeit = forms.IntegerField(required=True)
    einheit_l_b_h = forms.IntegerField(required=True)
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
    bemerkung = forms.CharField(required=False)

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

    begru = forms.ModelChoiceField(queryset=BEGRU.objects.all(), required=True)
    materialart_grunddaten = forms.ModelChoiceField(queryset=Materialart.objects.all(), required=True)
    sparte = forms.ModelChoiceField(queryset=Sparte.objects.all(), required=True)
    produkthierarchie = forms.CharField(required=True)
    materialzustandsverwaltung = forms.ModelChoiceField(queryset=Materialzustandsverwaltung.objects.all(), required=True)
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
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'materialzustandsverwaltung', 'rueckfuehrungscode', 'serialnummerprofil', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werk_1', 'werk_2', 'werk_3', 'werk_4', 'allgemeine_positionstypengruppe', 'verkaufsorg', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'cpv_code', 'spare_part_class_code', 'fertigungssteuerer', 'cpv_code', 'kennzeichen_komplexes_system', 'sonderablauf', 'cpv_code', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
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
'spare_part_class_code':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
        fields = ['positions_nr', 'hersteller', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile', 'grunddatentext_de_2_zeile', 'grunddatentext_fr_1_zeile', 'grunddatentext_fr_2_zeile', 'grunddatentext_en_1_zeile', 'grunddatentext_en_2_zeile', 'basismengeneinheit', 'bruttogewicht', 'gewichtseinheit', 'nettogewicht', 'groesse_abmessung', 'ean_upc_code', 'nato_stock_number', 'nsn_gruppe_klasse', 'nato_versorgungs_nr', 'herstellerteilenummer', 'normbezeichnung', 'gefahrgutkennzeichen', 'bruttogewicht', 'instandsetzbar', 'chargenpflicht', 'bestellmengeneinheit', 'mindestbestellmenge', 'lieferzeit', 'einheit_l_b_h', 'laenge', 'breite', 'hoehe', 'preis', 'waehrung', 'preiseinheit', 'lagerfaehigkeit', 'exportkontrollauflage', 'cage_code', 'hersteller_name', 'hersteller_adresse', 'hersteller_plz', 'hersteller_ort', 'revision', 'bemerkung', 'begru', 'materialart_grunddaten', 'sparte', 'produkthierarchie', 'materialzustandsverwaltung', 'rueckfuehrungscode', 'serialnummerprofil', 'hersteller_nr_gp', 'warengruppe', 'uebersetzungsstatus', 'endbevorratet', 'revision_fremd', 'revision_eigen', 'zertifiziert_fuer_flug', 'a_nummer', 'verteilung_an_psd', 'verteilung_an_ruag', 'werk_1', 'werk_2', 'werk_3', 'werk_4', 'allgemeine_positionstypengruppe', 'verkaufsorg', 'vertriebsweg', 'allgemeine_positionstypengruppe', 'fuehrendes_material', 'auszeichnungsfeld', 'cpv_code', 'spare_part_class_code', 'fertigungssteuerer', 'cpv_code', 'kennzeichen_komplexes_system', 'sonderablauf', 'cpv_code', 'temperaturbedingung', 'bewertungsklasse', 'systemmanager', 'kennziffer_bamf', 'mietrelevanz', 'next_higher_assembly', 'nachschubklasse', 'verteilung_apm_kerda', 'verteilung_svsaa', 'verteilung_cheops', 'zuteilung', 'auspraegung']
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
