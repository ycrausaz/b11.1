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
from .forms import CustomBooleanChoiceField, SplitterReadOnlyReadWriteFields, BaseTemplateForm
from .editable_fields_config import *

class MaterialForm_SMDA(BaseTemplateForm, SplitterReadOnlyReadWriteFields):

    # Start IL
#    positions_nr = forms.IntegerField(required=True)
#    kurztext_de = forms.CharField(required=True)
#    kurztext_fr = forms.CharField(required=True)
#    kurztext_en = forms.CharField(required=True)
#    grunddatentext_de_1_zeile = forms.CharField(required=True)
#    grunddatentext_de_2_zeile = forms.CharField(required=False)
#    grunddatentext_fr_1_zeile = forms.CharField(required=True)
#    grunddatentext_fr_2_zeile = forms.CharField(required=False)
#    grunddatentext_en_1_zeile = forms.CharField(required=True)
#    grunddatentext_en_2_zeile = forms.CharField(required=False)
#    basismengeneinheit = forms.ModelChoiceField(queryset=Basismengeneinheit.objects.all(), required=True)
#    bruttogewicht = forms.IntegerField(required=True)
#    #gewichtseinheit
#    nettogewicht = forms.IntegerField(required=False)
#    groesse_abmessung = forms.IntegerField(required=False)
#    ean_upc_code = forms.CharField(required=False)
#    nato_stock_number = forms.CharField(required=False)
#    #nsn_gruppe_klasse
#    #nato_versorgungs_nr
#    herstellerteilenummer = forms.CharField(required=True)
#    normbezeichnung = forms.CharField(required=False)
#    gefahrgutkennzeichen = forms.ModelChoiceField(queryset=Gefahrgutkennzeichen.objects.all(), required=False)
#    instandsetzbar = CustomBooleanChoiceField(required=True)
#    chargenpflicht = CustomBooleanChoiceField(required=True)
#    bestellmengeneinheit = forms.IntegerField(required=False)
#    mindestbestellmenge = forms.IntegerField(required=False)
#    lieferzeit = forms.IntegerField(required=True)
#    #einheit_l_b_h
#    laenge = forms.IntegerField(required=True)
#    breite = forms.IntegerField(required=True)
#    hoehe = forms.IntegerField(required=True)
#    preis = forms.IntegerField(required=True)
#    #waehrung
#    preiseinheit = forms.IntegerField(required=True)
#    lagerfaehigkeit = forms.IntegerField(required=True)
#    exportkontrollauflage = CustomBooleanChoiceField(required=False)
#    cage_code = forms.CharField(required=False)
#    hersteller_name = forms.CharField(required=True)
#    hersteller_adresse = forms.CharField(required=True)
#    hersteller_plz = forms.IntegerField(required=True)
#    hersteller_ort = forms.CharField(required=True)
#    revision = forms.CharField(required=False)
#    bemerkung = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)
    # End IL
    # Start GD
#    begru = forms.ModelChoiceField(queryset=BEGRU.objects.all(), required=True)
#    sparte = forms.ModelChoiceField(queryset=Sparte.objects.all(), required=True)
#    hersteller_nr_gp = forms.CharField(required=True)
#    warengruppe = forms.CharField(required=True)
#    uebersetzungsstatus = forms.ModelChoiceField(queryset=Uebersetzungsstatus.objects.all(), required=True)
#    verteilung_an_psd = CustomBooleanChoiceField(required=False)
#    revision_eigen = forms.CharField(required=False)
#    zertifiziert_fuer_flug = CustomBooleanChoiceField(required=False)
#    verteilung_an_ruag = CustomBooleanChoiceField(required=False)
#    #revision_fremd
#    a_nummer = forms.CharField(required=False)
#    materialart_grunddaten = forms.ModelChoiceField(queryset=Materialart.objects.all(), required=True)
#    produkthierarchie = forms.CharField(required=True)
#    rueckfuehrungscode = forms.ModelChoiceField(queryset=Rueckfuehrungscode.objects.all(), required=False)
#    serialnummerprofil = forms.ModelChoiceField(queryset=Serialnummerprofil.objects.all(), required=True)
#    endbevorratet = forms.CharField(required=False)
    #materialzustandsverwaltung
    # End GD
    # Start SMDA
    werkzuordnung_1 = forms.ModelChoiceField(queryset=Werkzuordnung_1.objects.all(), required=True)
    werkzuordnung_2 = forms.ModelChoiceField(queryset=Werkzuordnung_2.objects.all(), required=False)
    werkzuordnung_3 = forms.ModelChoiceField(queryset=Werkzuordnung_3.objects.all(), required=False)
    werkzuordnung_4 = forms.ModelChoiceField(queryset=Werkzuordnung_4.objects.all(), required=False)
    allgemeine_positionstypengruppe = forms.ModelChoiceField(queryset=AllgemeinePositionstypengruppe.objects.all(), required=True)
    spare_part_class_code = forms.ModelChoiceField(queryset=SparePartClassCode.objects.all(), required=True)
    fertigungssteuerer = forms.ModelChoiceField(queryset=Fertigungssteuerer.objects.all(), required=True)
    sonderablauf = forms.ModelChoiceField(queryset=Sonderablauf.objects.all(), required=False)
    temperaturbedingung = forms.ModelChoiceField(queryset=Temperaturbedingung.objects.all(), required=False)
    systemmanager = forms.CharField(required=False)
    mietrelevanz = CustomBooleanChoiceField(required=False)
    nachschubklasse = forms.CharField(required=False)
    materialeinstufung_nach_zuva = forms.ModelChoiceField(queryset=MaterialeinstufungNachZUVA.objects.all(), required=True)
    orderbuchpflicht = CustomBooleanChoiceField(required=False)
    verteilung_apm_kerda = CustomBooleanChoiceField(required=False)
    verteilung_svsaa = CustomBooleanChoiceField(required=False)
    verteilung_cheops = CustomBooleanChoiceField(required=False)
    zuteilung = forms.ModelChoiceField(queryset=Zuteilung.objects.all(), required=True)
    auspraegung = forms.ModelChoiceField(queryset=Auspraegung.objects.all(), required=True)
    #verkaufsorg
    #vertriebsweg
    #auszeichnungsfeld
    #preissteuerung
    #preisermittlung
    bewertungsklasse = forms.ModelChoiceField(queryset=Bewertungsklasse.objects.all(), required=True)
    fuehrendes_material = forms.CharField(required=False)
    kennzeichen_komplexes_system = CustomBooleanChoiceField(required=False)
    kennziffer_bamf = forms.CharField(required=False)
    next_higher_assembly = forms.CharField(required=False)
    # End SMDA

    class Meta(BaseTemplateForm.Meta):
        model = Material
        fields = EDITABLE_FIELDS

        widgets = {
            # Start IL
            'positions_nr':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
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
            'hersteller_nr_gp':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'hersteller_plz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'hersteller_ort':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'revision':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'bemerkung': forms.Textarea(attrs={'class':'form-control','rows':5,'readonly':True,'style':readonly_field_style()}),
            # End IL
            # Start GD
            'begru':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'sparte':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'hersteller':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}), #'hersteller_nr_gp'
            'warengruppe':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'uebersetzungsstatus':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'verteilung_an_psd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'revision_eigen':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'zertifiziert_fuer_flug':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'verteilung_an_ruag':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'revision_fremd':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'a_nummer':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'materialart_grunddaten':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'produkthierarchie':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'rueckfuehrungscode':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'serialnummerprofil':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'endbevorratet':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'materialzustandsverwaltung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            # End GD
            # Start SMDA
#            'werkzuordnung_1':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'werkzuordnung_2':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'werkzuordnung_3':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'werkzuordnung_4':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'allgemeine_positionstypengruppe':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'spare_part_class_code':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'fertigungssteuerer':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'sonderablauf':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'temperaturbedingung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'systemmanager':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'mietrelevanz':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'nachschubklasse':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'materialeinstufung_nach_zuva':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'orderbuchpflicht':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'verteilung_apm_kerda':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'verteilung_svsaa':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'verteilung_cheops':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'zuteilung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'auspraegung':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
            'verkaufsorg':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'vertriebsweg':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'auszeichnungsfeld':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'preissteuerung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            'preisermittlung':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'bewertungsklasse':ReadOnlyForeignKeyWidget(attrs={'readonly':True,'style':readonly_field_style()}),
#            'fuehrendes_material':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'kennzeichen_komplexes_system':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'kennziffer_bamf':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
#            'next_higher_assembly':forms.TextInput(attrs={'readonly':True,'style':readonly_field_style()}),
            # End SMDA
        }

    def __init__(self, *args, **kwargs):
        kwargs['editable_fields'] = EDITABLE_FIELDS_SMDA
        super().__init__(*args, **kwargs)
        tooltips = HelpTooltip.objects.all()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                field.help_text = tooltip.content
