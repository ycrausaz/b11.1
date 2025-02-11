# symm/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

MAX_ATTACHMENTS_PER_MATERIAL = 5
MAX_ATTACHMENT_SIZE = 2.5 * 1024 * 1024  # 2.5MB in bytes

class LogEntry(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=_('ID'))
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    message = models.TextField()

    class Meta:
        app_label = 'symm'
        db_table = 'symm_log_entries'

class BaseIdxModel(models.Model):
    """Abstract base class for models with idx field"""
    idx = models.IntegerField(unique=True, null=True, blank=True)
    text = models.CharField(null=True, blank=True, max_length=40)
    explanation = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        if self.explanation:
            return f"{self.text} - {self.explanation}"
        return self.text or str(self.idx)

    class Meta:
        abstract = True
        ordering = ['idx']

class Profile(models.Model):
    USER_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    firm = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_first_login = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)
    registration_token = models.CharField(max_length=100, null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class HelpTooltip(models.Model):
    field_name = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return f"Help for {self.field_name}"

    class Meta:
        app_label = 'symm'

class G_Partner(models.Model):
    cage_code = models.CharField(null=True, blank=True, max_length=40)
    gp_nummer = models.CharField(null=True, blank=True, max_length=40)
    kreditor_nr = models.CharField(null=True, blank=True, max_length=40)
    name = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        app_label = 'symm'

class BEGRU(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Basismengeneinheit(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Materialart(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Sparte(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Rueckfuehrungscode(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Serialnummerprofil(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class SparePartClassCode(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Uebersetzungsstatus(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Gefahrgutkennzeichen(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Werkzuordnung_1(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Werkzuordnung_2(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Werkzuordnung_3(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Werkzuordnung_4(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class AllgemeinePositionstypengruppe(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Fertigungssteuerer(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Sonderablauf(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Temperaturbedingung(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Bewertungsklasse(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Zuteilung(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Auspraegung(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class MaterialeinstufungNachZUVA(BaseIdxModel):
    class Meta:
        app_label = 'symm'

class Material(models.Model):
    hersteller = models.CharField(null=True, blank=True, max_length=40)
    is_transferred = models.BooleanField(null=True, blank=False, default=False)
    is_archived = models.BooleanField(null=True, blank=False, default=False)
    transfer_date = models.DateTimeField(null=True, blank=True)
    transfer_comment = models.TextField(null=True, blank=True, max_length=4096, verbose_name=_("Transfer Comment"))
    positions_nr = models.IntegerField(null=True, blank=True, verbose_name=_("Positions-Nr."))
    kurztext_de = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Kurztext DE"))
    kurztext_fr = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Kurztext FR"))
    kurztext_en = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Kurztext EN"))
    grunddatentext_de_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext DE - 1. Zeile"))
    grunddatentext_de_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext DE - 2. Zeile"))
    grunddatentext_fr_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext FR - 1. Zeile"))
    grunddatentext_fr_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext FR - 2. Zeile"))
    grunddatentext_en_1_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext EN - 1. Zeile"))
    grunddatentext_en_2_zeile = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Grunddatentext EN - 2. Zeile"))
    basismengeneinheit = models.ForeignKey(Basismengeneinheit, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Basismengeneinheit"))
    bruttogewicht = models.IntegerField(null=True, blank=True, verbose_name=_("Bruttogewicht"))
    gewichtseinheit = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Gewichtseinheit"))
    nettogewicht = models.IntegerField(null=True, blank=True, verbose_name=_("Nettogewicht"))
    groesse_abmessung = models.IntegerField(null=True, blank=True, verbose_name=_("Grösse / Abmessung"))
    ean_upc_code = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("EAN / UPC Code"))
    nato_stock_number = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Nato Stock Number"))
    nsn_gruppe_klasse = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("NSN Gruppe / Klasse"))
    nato_versorgungs_nr = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Nato Versorgungs-Nr."))
    herstellerteilenummer = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Herstellerteilenummer"))
    normbezeichnung = models.CharField(null=True, blank=True, max_length=18, verbose_name=_("Normbezeichnung"))
    gefahrgutkennzeichen = models.ForeignKey(Gefahrgutkennzeichen, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Gefahrgutkennzeichen"))
    instandsetzbar = models.BooleanField(null=True, blank=True, verbose_name=_("Instandsetzbar"))
    chargenpflicht = models.BooleanField(null=True, blank=True, verbose_name=_("Chargenpflicht"))
    bestellmengeneinheit = models.IntegerField(null=True, blank=True, verbose_name=_("Bestellmengeneinheit"))
    mindestbestellmenge = models.IntegerField(null=True, blank=True, verbose_name=_("Mindestbestellmenge"))
    lieferzeit = models.IntegerField(null=True, blank=True, verbose_name=_("Lieferzeit"))
    einheit_l_b_h = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Einheit L / B / H"))
    laenge = models.IntegerField(null=True, blank=True, verbose_name=_("Länge"))
    breite = models.IntegerField(null=True, blank=True, verbose_name=_("Breite"))
    hoehe = models.IntegerField(null=True, blank=True, verbose_name=_("Höhe"))
    preis = models.FloatField(null=True, blank=True, verbose_name=_("Preis"))
    waehrung = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Währung"))
    preiseinheit = models.IntegerField(null=True, blank=True, verbose_name=_("Preiseinheit"))
    lagerfaehigkeit = models.IntegerField(null=True, blank=True, verbose_name=_("Lagerfähigkeit"))
    exportkontrollauflage = models.BooleanField(null=True, blank=True, verbose_name=_("Exportkontrollauflage"))
    cage_code = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("CAGE Code"))
    hersteller_name = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Hersteller Name"))
    hersteller_adresse = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Hersteller Adresse"))
    hersteller_plz = models.IntegerField(null=True, blank=True, verbose_name=_("Hersteller PLZ "))
    hersteller_ort = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Hersteller Ort"))
    revision = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Revision"))
    bemerkung = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Bemerkung"))
    begru = models.ForeignKey(BEGRU, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("BEGRU"))
    materialart_grunddaten = models.ForeignKey(Materialart, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Materialart"))
    sparte = models.ForeignKey(Sparte, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Sparte"))
    produkthierarchie = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Produkthierarchie"))
    materialzustandsverwaltung = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Materialzustandsverwaltung"))
    rueckfuehrungscode = models.ForeignKey(Rueckfuehrungscode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Rückführungscode"))
    serialnummerprofil = models.ForeignKey(Serialnummerprofil, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Serialnummerprofil"))
    spare_part_class_code = models.ForeignKey(SparePartClassCode, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Spare Part Class Code"))
    geschaeftspartner = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Geschäftspartner"))
    warengruppe = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Warengruppe"))
    uebersetzungsstatus = models.ForeignKey(Uebersetzungsstatus, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Übersetzungsstatus"))
    endbevorratet = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Endbevorratet"))
    revision_fremd = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Revision Fremd"))
    revision_eigen = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Revision Eigen"))
    zertifiziert_fuer_flug = models.BooleanField(null=True, blank=True, verbose_name=_("Zertifiziert für Flug"))
    a_nummer = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("A-Nummer"))
    verteilung_an_psd = models.BooleanField(null=True, blank=True, verbose_name=_("Verteilung an PSD"))
    verteilung_an_ruag = models.BooleanField(null=True, blank=True, verbose_name=_("Verteilung an RUAG"))
    werkzuordnung_1 = models.ForeignKey(Werkzuordnung_1, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Werkzuordnung"))
    werkzuordnung_2 = models.ForeignKey(Werkzuordnung_2, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Werkzuordnung (2)"))
    werkzuordnung_3 = models.ForeignKey(Werkzuordnung_3, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Werkzuordnung (3)"))
    werkzuordnung_4 = models.ForeignKey(Werkzuordnung_4, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Werkzuordnung (4)"))
    allgemeine_positionstypengruppe = models.ForeignKey(AllgemeinePositionstypengruppe, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Allgemeine Positionstypengruppe"))
    verkaufsorg = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Verkaufsorg."))
    vertriebsweg = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Vertriebsweg"))
    fuehrendes_material = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Führendes Material"))
    auszeichnungsfeld = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Auszeichnungsfeld"))
    fertigungssteuerer = models.ForeignKey(Fertigungssteuerer, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Fertigungssteuerer"))
    kennzeichen_komplexes_system = models.BooleanField(null=True, blank=True, verbose_name=_("Kennzeichen komplexes System"))
    sonderablauf = models.ForeignKey(Sonderablauf, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Sonderablauf"))
    temperaturbedingung = models.ForeignKey(Temperaturbedingung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Temperaturbedingung"))
    bewertungsklasse = models.ForeignKey(Bewertungsklasse, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Bewertungsklasse"))
    systemmanager = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Systemmanager"))
    kennziffer_bamf = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Kennziffer BAMF"))
    mietrelevanz = models.BooleanField(null=True, blank=True, verbose_name=_("Mietrelevanz"))
    next_higher_assembly = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Next Higher Assembly"))
    nachschubklasse = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Nachschubklasse"))
    materialeinstufung_nach_zuva = models.ForeignKey(MaterialeinstufungNachZUVA, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Materialeinstufung nach ZUVA"))
    orderbuchpflicht = models.BooleanField(null=True, blank=True, verbose_name=_("Orderbuchpflicht"))
    verteilung_apm_kerda = models.BooleanField(null=True, blank=True, verbose_name=_("Verteilung APM Kerda"))
    verteilung_svsaa = models.BooleanField(null=True, blank=True, verbose_name=_("Verteilung SVSAA"))
    verteilung_cheops = models.BooleanField(null=True, blank=True, verbose_name=_("Verteilung CHEOPS"))
    zuteilung = models.ForeignKey(Zuteilung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Zuteilung"))
    auspraegung = models.ForeignKey(Auspraegung, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Ausprägung"))
    preissteuerung = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Preissteuerung"))
    preisermittlung = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Preisermittlung"))

    def __str__(self):
        if self.positions_nr is not None:
            return str(self.positions_nr) + " - " + self.kurztext_de + " (" + self.hersteller + ")"
        else:
            return "<None> - " + self.kurztext_de + " (" + self.hersteller + ")"

    class Meta:
        ordering = ["positions_nr"]
        app_label = 'symm'

def material_attachment_path(instance, filename):
    """
    Files will be uploaded to MEDIA_ROOT/material_attachments/material_id/filename
    """
    return f'material_attachments/{instance.material.id}/{filename}'

class MaterialAttachment(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=material_attachment_path)
    comment = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.file:
            if self.file.size > MAX_ATTACHMENT_SIZE:
                raise ValidationError(f'File size cannot exceed {MAX_ATTACHMENT_SIZE/1024/1024:.1f}MB')
            
            # Count existing attachments for this material
            if not self.id:  # Only check on new attachments
                existing_count = MaterialAttachment.objects.filter(material=self.material).count()
                if existing_count >= MAX_ATTACHMENTS_PER_MATERIAL:
                    raise ValidationError(f'Cannot have more than {MAX_ATTACHMENTS_PER_MATERIAL} attachments per material')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'symm'
        ordering = ['-uploaded_at']
