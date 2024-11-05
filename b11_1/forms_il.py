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
from .editable_fields_config import *

class MaterialForm_IL(ModelForm, SplitterReadOnlyReadWriteFields):

    # Start IL
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
    #gewichtseinheit
    nettogewicht = forms.IntegerField(required=False)
    groesse_abmessung = forms.IntegerField(required=False)
    ean_upc_code = forms.CharField(required=False)
    nato_stock_number = forms.CharField(required=False)
    #nsn_gruppe_klasse
    #nato_versorgungs_nr
    herstellerteilenummer = forms.CharField(required=True)
    normbezeichnung = forms.CharField(required=False)
    gefahrgutkennzeichen = forms.ModelChoiceField(queryset=Gefahrgutkennzeichen.objects.all(), required=False)
    instandsetzbar = CustomBooleanChoiceField(required=True)
    chargenpflicht = CustomBooleanChoiceField(required=True)
    bestellmengeneinheit = forms.IntegerField(required=False)
    mindestbestellmenge = forms.IntegerField(required=False)
    lieferzeit = forms.IntegerField(required=True)
    #einheit_l_b_h
    laenge = forms.IntegerField(required=True)
    breite = forms.IntegerField(required=True)
    hoehe = forms.IntegerField(required=True)
    preis = forms.IntegerField(required=True)
    #waehrung
    preiseinheit = forms.IntegerField(required=True)
    lagerfaehigkeit = forms.IntegerField(required=True)
    exportkontrollauflage = CustomBooleanChoiceField(required=False)
    cage_code = forms.CharField(required=False)
    hersteller_name = forms.CharField(required=True)
    hersteller_adresse = forms.CharField(required=True)
    hersteller_plz = forms.IntegerField(required=True)
    hersteller_ort = forms.CharField(required=True)
    revision = forms.CharField(required=False)
    bemerkung = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)
    # End IL
    # Start GD
#    begru = forms.ModelChoiceField(queryset=BEGRU.objects.all(), required=True)
#    sparte = forms.ModelChoiceField(queryset=Sparte.objects.all(), required=True)
#    geschaeftspartner = forms.CharField(required=True)
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
#    #materialzustandsverwaltung
    # End GD
    # Start SMDA
#    werkzuordnung_1 = forms.ModelChoiceField(queryset=Werkzuordnung_1.objects.all(), required=True)
#    werkzuordnung_2 = forms.ModelChoiceField(queryset=Werkzuordnung_2.objects.all(), required=False)
#    werkzuordnung_3 = forms.ModelChoiceField(queryset=Werkzuordnung_3.objects.all(), required=False)
#    werkzuordnung_4 = forms.ModelChoiceField(queryset=Werkzuordnung_4.objects.all(), required=false)
#    allgemeine_positionstypengruppe = forms.ModelChoiceField(queryset=AllgemeinePositionstypengruppe.objects.all(), required=True)
#    spare_part_class_code = forms.ModelChoiceField(queryset=SparePartClassCode.objects.all(), required=True)
#    fertigungssteuerer = forms.ModelChoiceField(queryset=Fertigungssteuerer.objects.all(), required=True)
#    sonderablauf = forms.ModelChoiceField(queryset=Sonderablauf.objects.all(), required=False)
#    temperaturbedingung = forms.ModelChoiceField(queryset=Temperaturbedingung.objects.all(), required=False)
#    systemmanager = forms.CharField(required=False)
#    mietrelevanz = CustomBooleanChoiceField(required=False)
#    nachschubklasse = forms.CharField(required=False)
#    materialeinstufung_nach_zuva = forms.ModelChoiceField(queryset=MaterialeinstufungNachZUVA.objects.all(), required=True)
#    orderbuchpflicht = CustomBooleanChoiceField(required=False)
#    verteilung_apm_kerda = CustomBooleanChoiceField(required=False)
#    verteilung_svsaa = CustomBooleanChoiceField(required=False)
#    verteilung_cheops = CustomBooleanChoiceField(required=False)
#    zuteilung = forms.ModelChoiceField(queryset=Zuteilung.objects.all(), required=True)
#    auspraegung = forms.ModelChoiceField(queryset=Auspraegung.objects.all(), required=True)
#    #verkaufsorg
#    #vertriebsweg
#    #auszeichnungsfeld
#    #preissteuerung
#    #preisermittlung
#    bewertungsklasse = forms.ModelChoiceField(queryset=Bewertungsklasse.objects.all(), required=True)
#    fuehrendes_material = forms.CharField(required=False)
#    kennzeichen_komplexes_system = CustomBooleanChoiceField(required=False)
#    kennziffer_bamf = forms.CharField(required=False)
#    next_higher_assembly = forms.CharField(required=False)
    # End SMDA

    class Meta:
        model = Material
        fields = EDITABLE_FIELDS_IL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tooltips = HelpTooltip.objects.all()
        for field_name, field in self.fields.items():
            tooltip = tooltips.filter(field_name=field_name).first()
            if tooltip:
                field.help_text = tooltip.content
