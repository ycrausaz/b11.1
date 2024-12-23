# b11_1/models.py

from django.db import models
from django.contrib.auth.models import User

class LogEntry(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    message = models.TextField()

    class Meta:
        app_label = 'b11_1'
        db_table = 'b11_1_log_entries'

class BaseIdxModel(models.Model):
    """Abstract base class for models with idx field"""
    idx = models.IntegerField(unique=True, null=True, blank=True)
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True
        ordering = ['idx']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_first_login = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'b11_1'

class HelpTooltip(models.Model):
    field_name = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return f"Help for {self.field_name}"

    class Meta:
        app_label = 'b11_1'

class G_Partner(models.Model):
    cage_code = models.CharField(null=True, blank=True, max_length=40)
    gp_nummer = models.CharField(null=True, blank=True, max_length=40)
    kreditor_nr = models.CharField(null=True, blank=True, max_length=40)
    name = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        app_label = 'b11_1'

class BEGRU(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Basismengeneinheit(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Materialart(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Sparte(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Rueckfuehrungscode(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Serialnummerprofil(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class SparePartClassCode(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Uebersetzungsstatus(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Gefahrgutkennzeichen(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Werkzuordnung_1(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Werkzuordnung_2(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Werkzuordnung_3(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Werkzuordnung_4(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class AllgemeinePositionstypengruppe(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Fertigungssteuerer(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Sonderablauf(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Temperaturbedingung(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Bewertungsklasse(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Zuteilung(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Auspraegung(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class MaterialeinstufungNachZUVA(BaseIdxModel):
    class Meta:
        app_label = 'b11_1'

class Material(models.Model):
    hersteller = models.CharField(null=True, blank=True, max_length=40)
    is_transferred = models.BooleanField(null=True, blank=False, default=False)
    is_archived = models.BooleanField(null=True, blank=False, default=False)
    transfer_date = models.DateTimeField(null=True, blank=True)
    positions_nr = models.IntegerField(null=True, blank=True)
    kurztext_de = models.CharField(null=True, blank=True, max_length=40)
    kurztext_fr = models.CharField(null=True, blank=True, max_length=40)
    kurztext_en = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_de_1_zeile = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_de_2_zeile = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_fr_1_zeile = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_fr_2_zeile = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_en_1_zeile = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_en_2_zeile = models.CharField(null=True, blank=True, max_length=40)
    basismengeneinheit = models.ForeignKey(Basismengeneinheit, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Basismengeneinheit ")
    bruttogewicht = models.IntegerField(null=True, blank=True)
    gewichtseinheit = models.CharField(null=True, blank=True, max_length=40)
    nettogewicht = models.IntegerField(null=True, blank=True)
    groesse_abmessung = models.IntegerField(null=True, blank=True)
    ean_upc_code = models.CharField(null=True, blank=True, max_length=40)
    nato_stock_number = models.CharField(null=True, blank=True, max_length=40)
    nsn_gruppe_klasse = models.CharField(null=True, blank=True, max_length=40)
    nato_versorgungs_nr = models.CharField(null=True, blank=True, max_length=40)
    herstellerteilenummer = models.CharField(null=True, blank=True, max_length=40)
    normbezeichnung = models.CharField(null=True, blank=True, max_length=18)
    gefahrgutkennzeichen = models.ForeignKey(Gefahrgutkennzeichen, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Gefahrgutkennzeichen ")
    instandsetzbar = models.BooleanField(null=True, blank=True)
    chargenpflicht = models.BooleanField(null=True, blank=True)
    bestellmengeneinheit = models.IntegerField(null=True, blank=True)
    mindestbestellmenge = models.IntegerField(null=True, blank=True)
    lieferzeit = models.IntegerField(null=True, blank=True)
    einheit_l_b_h = models.CharField(null=True, blank=True, max_length=40)
    laenge = models.IntegerField(null=True, blank=True)
    breite = models.IntegerField(null=True, blank=True)
    hoehe = models.IntegerField(null=True, blank=True)
    preis = models.FloatField(null=True, blank=True)
    waehrung = models.CharField(null=True, blank=True, max_length=40)
    preiseinheit = models.IntegerField(null=True, blank=True)
    lagerfaehigkeit = models.IntegerField(null=True, blank=True)
    exportkontrollauflage = models.BooleanField(null=True, blank=True)
    cage_code = models.CharField(null=True, blank=True, max_length=40)
    hersteller_name = models.CharField(null=True, blank=True, max_length=40)
    hersteller_adresse = models.CharField(null=True, blank=True, max_length=40)
    hersteller_plz = models.IntegerField(null=True, blank=True)
    hersteller_ort = models.CharField(null=True, blank=True, max_length=40)
    revision = models.CharField(null=True, blank=True, max_length=30)
    bemerkung = models.CharField(null=True, blank=True, max_length=40)
    begru = models.ForeignKey(BEGRU, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="BEGRU ")
    materialart_grunddaten = models.ForeignKey(Materialart, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Materialart ")
    sparte = models.ForeignKey(Sparte, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Sparte ")
    produkthierarchie = models.CharField(null=True, blank=True, max_length=40)
    materialzustandsverwaltung = models.CharField(null=True, blank=True, max_length=40)
    rueckfuehrungscode = models.ForeignKey(Rueckfuehrungscode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Rückführungscode ")
    serialnummerprofil = models.ForeignKey(Serialnummerprofil, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Serialnummerprofil ")
    spare_part_class_code = models.ForeignKey(SparePartClassCode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Spare Part Class Code ")
    geschaeftspartner = models.CharField(null=True, blank=True, max_length=40)
    warengruppe = models.CharField(null=True, blank=True, max_length=40)
    uebersetzungsstatus = models.ForeignKey(Uebersetzungsstatus, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Übersetzungsstatus ")
    endbevorratet = models.CharField(null=True, blank=True, max_length=40)
    revision_fremd = models.CharField(null=True, blank=True, max_length=40)
    revision_eigen = models.CharField(null=True, blank=True, max_length=40)
    zertifiziert_fuer_flug = models.BooleanField(null=True, blank=True)
    a_nummer = models.CharField(null=True, blank=True, max_length=40)
    verteilung_an_psd = models.BooleanField(null=True, blank=True)
    verteilung_an_ruag = models.BooleanField(null=True, blank=True)
    werkzuordnung_1 = models.ForeignKey(Werkzuordnung_1, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung ")
    werkzuordnung_2 = models.ForeignKey(Werkzuordnung_2, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (2) ")
    werkzuordnung_3 = models.ForeignKey(Werkzuordnung_3, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (3) ")
    werkzuordnung_4 = models.ForeignKey(Werkzuordnung_4, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (4) ")
    allgemeine_positionstypengruppe = models.ForeignKey(AllgemeinePositionstypengruppe, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Allgemeine Positionstypengruppe ")
    verkaufsorg = models.CharField(null=True, blank=True, max_length=40)
    vertriebsweg = models.CharField(null=True, blank=True, max_length=40)
    fuehrendes_material = models.CharField(null=True, blank=True, max_length=40)
    auszeichnungsfeld = models.CharField(null=True, blank=True, max_length=40)
    fertigungssteuerer = models.ForeignKey(Fertigungssteuerer, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Fertigungssteuerer ")
    kennzeichen_komplexes_system = models.BooleanField(null=True, blank=True)
    sonderablauf = models.ForeignKey(Sonderablauf, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Sonderablauf ")
    temperaturbedingung = models.ForeignKey(Temperaturbedingung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Temperaturbedingung ")
    bewertungsklasse = models.ForeignKey(Bewertungsklasse, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Bewertungsklasse ")
    systemmanager = models.CharField(null=True, blank=True, max_length=30)
    kennziffer_bamf = models.CharField(null=True, blank=True, max_length=30)
    mietrelevanz = models.BooleanField(null=True, blank=True)
    next_higher_assembly = models.CharField(null=True, blank=True, max_length=30)
    nachschubklasse = models.CharField(null=True, blank=True, max_length=30)
    materialeinstufung_nach_zuva = models.ForeignKey(MaterialeinstufungNachZUVA, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Materialeinstufung nach ZUVA ")
    orderbuchpflicht = models.BooleanField(null=True, blank=True)
    verteilung_apm_kerda = models.BooleanField(null=True, blank=True)
    verteilung_svsaa = models.BooleanField(null=True, blank=True)
    verteilung_cheops = models.BooleanField(null=True, blank=True)
    zuteilung = models.ForeignKey(Zuteilung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Zuteilung ")
    auspraegung = models.ForeignKey(Auspraegung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Ausprägung ")
    preissteuerung = models.CharField(null=True, blank=True, max_length=40)
    preisermittlung = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self):
        if self.positions_nr is not None:
            return str(self.positions_nr) + " - " + self.kurztext_de + " (" + self.hersteller + ")"
        else:
            return "<None> - " + self.kurztext_de + " (" + self.hersteller + ")"

    class Meta:
        ordering = ["positions_nr"]
        app_label = 'b11_1'

