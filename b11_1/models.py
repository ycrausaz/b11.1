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
    transfer_comment = models.TextField(null=True, blank=True, max_length=4096, verbose_name="Transfer Comment")
    positions_nr = models.IntegerField(null=True, blank=True, verbose_name="Positions-Nr. ")
    kurztext_de = models.CharField(null=True, blank=True, max_length=40, verbose_name="Kurztext DE ")
    kurztext_fr = models.CharField(null=True, blank=True, max_length=40, verbose_name="Kurztext FR ")
    kurztext_en = models.CharField(null=True, blank=True, max_length=40, verbose_name="Kurztext EN ")
    grunddatentext_de_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext DE - 1. Zeile ")
    grunddatentext_de_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext DE - 2. Zeile ")
    grunddatentext_fr_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext FR - 1. Zeile ")
    grunddatentext_fr_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext FR - 2. Zeile ")
    grunddatentext_en_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext EN - 1. Zeile ")
    grunddatentext_en_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name="Grunddatentext EN - 2. Zeile ")
    basismengeneinheit = models.ForeignKey(Basismengeneinheit, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Basismengeneinheit ")
    bruttogewicht = models.IntegerField(null=True, blank=True, verbose_name="Bruttogewicht ")
    gewichtseinheit = models.CharField(null=True, blank=True, max_length=40, verbose_name="Gewichtseinheit ")
    nettogewicht = models.IntegerField(null=True, blank=True, verbose_name="Nettogewicht ")
    groesse_abmessung = models.IntegerField(null=True, blank=True, verbose_name="Grösse / Abmessung ")
    ean_upc_code = models.CharField(null=True, blank=True, max_length=40, verbose_name="EAN / UPC Code ")
    nato_stock_number = models.CharField(null=True, blank=True, max_length=40, verbose_name="Nato Stock Number ")
    nsn_gruppe_klasse = models.CharField(null=True, blank=True, max_length=40, verbose_name="NSN Gruppe / Klasse ")
    nato_versorgungs_nr = models.CharField(null=True, blank=True, max_length=40, verbose_name="Nato Versorgungs-Nr. ")
    herstellerteilenummer = models.CharField(null=True, blank=True, max_length=40, verbose_name="Herstellerteilenummer ")
    normbezeichnung = models.CharField(null=True, blank=True, max_length=18, verbose_name="Normbezeichnung ")
    gefahrgutkennzeichen = models.ForeignKey(Gefahrgutkennzeichen, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Gefahrgutkennzeichen ")
    instandsetzbar = models.BooleanField(null=True, blank=True, verbose_name="Instandsetzbar ")
    chargenpflicht = models.BooleanField(null=True, blank=True, verbose_name="Chargenpflicht ")
    bestellmengeneinheit = models.IntegerField(null=True, blank=True, verbose_name="Bestellmengeneinheit ")
    mindestbestellmenge = models.IntegerField(null=True, blank=True, verbose_name="Mindestbestellmenge ")
    lieferzeit = models.IntegerField(null=True, blank=True, verbose_name="Lieferzeit ")
    einheit_l_b_h = models.CharField(null=True, blank=True, max_length=40, verbose_name="Einheit L / B / H ")
    laenge = models.IntegerField(null=True, blank=True, verbose_name="Länge ")
    breite = models.IntegerField(null=True, blank=True, verbose_name="Breite ")
    hoehe = models.IntegerField(null=True, blank=True, verbose_name="Höhe ")
    preis = models.FloatField(null=True, blank=True, verbose_name="Preis ")
    waehrung = models.CharField(null=True, blank=True, max_length=40, verbose_name="Währung ")
    preiseinheit = models.IntegerField(null=True, blank=True, verbose_name="Preiseinheit ")
    lagerfaehigkeit = models.IntegerField(null=True, blank=True, verbose_name="Lagerfähigkeit ")
    exportkontrollauflage = models.BooleanField(null=True, blank=True, verbose_name="Exportkontrollauflage ")
    cage_code = models.CharField(null=True, blank=True, max_length=40, verbose_name="CAGE Code ")
    hersteller_name = models.CharField(null=True, blank=True, max_length=40, verbose_name="Hersteller Name ")
    hersteller_adresse = models.CharField(null=True, blank=True, max_length=40, verbose_name="Hersteller Adresse ")
    hersteller_plz = models.IntegerField(null=True, blank=True, verbose_name="Hersteller PLZ  ")
    hersteller_ort = models.CharField(null=True, blank=True, max_length=40, verbose_name="Hersteller Ort ")
    revision = models.CharField(null=True, blank=True, max_length=30, verbose_name="Revision ")
    bemerkung = models.CharField(null=True, blank=True, max_length=40, verbose_name="Bemerkung ")
    begru = models.ForeignKey(BEGRU, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="BEGRU ")
    materialart_grunddaten = models.ForeignKey(Materialart, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Materialart ")
    sparte = models.ForeignKey(Sparte, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Sparte ")
    produkthierarchie = models.CharField(null=True, blank=True, max_length=40, verbose_name="Produkthierarchie ")
    materialzustandsverwaltung = models.CharField(null=True, blank=True, max_length=40, verbose_name="Materialzustandsverwaltung ")
    rueckfuehrungscode = models.ForeignKey(Rueckfuehrungscode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Rückführungscode ")
    serialnummerprofil = models.ForeignKey(Serialnummerprofil, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Serialnummerprofil ")
    spare_part_class_code = models.ForeignKey(SparePartClassCode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Spare Part Class Code ")
    geschaeftspartner = models.CharField(null=True, blank=True, max_length=40, verbose_name="Geschäftspartner ")
    warengruppe = models.CharField(null=True, blank=True, max_length=40, verbose_name="Warengruppe ")
    uebersetzungsstatus = models.ForeignKey(Uebersetzungsstatus, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Übersetzungsstatus ")
    endbevorratet = models.CharField(null=True, blank=True, max_length=40, verbose_name="Endbevorratet ")
    revision_fremd = models.CharField(null=True, blank=True, max_length=40, verbose_name="Revision Fremd ")
    revision_eigen = models.CharField(null=True, blank=True, max_length=40, verbose_name="Revision Eigen ")
    zertifiziert_fuer_flug = models.BooleanField(null=True, blank=True, verbose_name="Zertifiziert für Flug ")
    a_nummer = models.CharField(null=True, blank=True, max_length=40, verbose_name="A-Nummer ")
    verteilung_an_psd = models.BooleanField(null=True, blank=True, verbose_name="Verteilung an PSD ")
    verteilung_an_ruag = models.BooleanField(null=True, blank=True, verbose_name="Verteilung an RUAG ")
    werkzuordnung_1 = models.ForeignKey(Werkzuordnung_1, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung ")
    werkzuordnung_2 = models.ForeignKey(Werkzuordnung_2, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (2) ")
    werkzuordnung_3 = models.ForeignKey(Werkzuordnung_3, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (3) ")
    werkzuordnung_4 = models.ForeignKey(Werkzuordnung_4, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Werkzuordnung (4) ")
    allgemeine_positionstypengruppe = models.ForeignKey(AllgemeinePositionstypengruppe, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Allgemeine Positionstypengruppe ")
    verkaufsorg = models.CharField(null=True, blank=True, max_length=40, verbose_name="Verkaufsorg. ")
    vertriebsweg = models.CharField(null=True, blank=True, max_length=40, verbose_name="Vertriebsweg ")
    fuehrendes_material = models.CharField(null=True, blank=True, max_length=40, verbose_name="Führendes Material ")
    auszeichnungsfeld = models.CharField(null=True, blank=True, max_length=40, verbose_name="Auszeichnungsfeld ")
    fertigungssteuerer = models.ForeignKey(Fertigungssteuerer, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Fertigungssteuerer ")
    kennzeichen_komplexes_system = models.BooleanField(null=True, blank=True, verbose_name="Kennzeichen komplexes System ")
    sonderablauf = models.ForeignKey(Sonderablauf, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Sonderablauf ")
    temperaturbedingung = models.ForeignKey(Temperaturbedingung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Temperaturbedingung ")
    bewertungsklasse = models.ForeignKey(Bewertungsklasse, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Bewertungsklasse ")
    systemmanager = models.CharField(null=True, blank=True, max_length=30, verbose_name="Systemmanager ")
    kennziffer_bamf = models.CharField(null=True, blank=True, max_length=30, verbose_name="Kennziffer BAMF ")
    mietrelevanz = models.BooleanField(null=True, blank=True, verbose_name="Mietrelevanz ")
    next_higher_assembly = models.CharField(null=True, blank=True, max_length=30, verbose_name="Next Higher Assembly ")
    nachschubklasse = models.CharField(null=True, blank=True, max_length=30, verbose_name="Nachschubklasse ")
    materialeinstufung_nach_zuva = models.ForeignKey(MaterialeinstufungNachZUVA, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Materialeinstufung nach ZUVA ")
    orderbuchpflicht = models.BooleanField(null=True, blank=True, verbose_name="Orderbuchpflicht ")
    verteilung_apm_kerda = models.BooleanField(null=True, blank=True, verbose_name="Verteilung APM Kerda ")
    verteilung_svsaa = models.BooleanField(null=True, blank=True, verbose_name="Verteilung SVSAA ")
    verteilung_cheops = models.BooleanField(null=True, blank=True, verbose_name="Verteilung CHEOPS ")
    zuteilung = models.ForeignKey(Zuteilung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Zuteilung ")
    auspraegung = models.ForeignKey(Auspraegung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Ausprägung ")
    preissteuerung = models.CharField(null=True, blank=True, max_length=40, verbose_name="Preissteuerung ")
    preisermittlung = models.CharField(null=True, blank=True, max_length=30, verbose_name="Preisermittlung ")

    def __str__(self):
        if self.positions_nr is not None:
            return str(self.positions_nr) + " - " + self.kurztext_de + " (" + self.hersteller + ")"
        else:
            return "<None> - " + self.kurztext_de + " (" + self.hersteller + ")"

    class Meta:
        ordering = ["positions_nr"]
        app_label = 'b11_1'

