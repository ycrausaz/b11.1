# b11_1/models.py

import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import boto3
from botocore.client import Config
from .utils.storage import MaterialAttachmentStorage

class LogEntry(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=_('ID'))
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
    firm = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
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
    help_content_de = models.TextField(blank=True, null=True, verbose_name=_("Help content (German)"))
    help_content_fr = models.TextField(blank=True, null=True, verbose_name=_("Help content (French)"))
    help_content_en = models.TextField(blank=True, null=True, verbose_name=_("Help content (English)"))
    inline_help_de = models.TextField(blank=True, null=True, verbose_name=_("Inline help (German)"))
    inline_help_fr = models.TextField(blank=True, null=True, verbose_name=_("Inline help (French)"))
    inline_help_en = models.TextField(blank=True, null=True, verbose_name=_("Inline help (English)"))

    def __str__(self):
        return f"Help for {self.field_name}"

    def get_help_content(self, language_code=None):
        """Get the help content in the specified language"""
        if not language_code:
            from django.utils.translation import get_language
            language_code = get_language()

        attr_name = f"help_content_{language_code}"
        if hasattr(self, attr_name) and getattr(self, attr_name):
            return getattr(self, attr_name)

        # Fallback to German if translation is missing
        return self.help_content_de or ""

    def get_inline_help(self, language_code=None):
        """Get the inline help in the specified language"""
        if not language_code:
            from django.utils.translation import get_language
            language_code = get_language()

        attr_name = f"inline_help_{language_code}"
        if hasattr(self, attr_name) and getattr(self, attr_name):
            return getattr(self, attr_name)

        # Fallback to German if translation is missing
        return self.inline_help_de or ""

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

class Bestellmengeneinheit(BaseIdxModel):
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
    is_finished = models.BooleanField(default=False, verbose_name=_("Fertig"))
    transfer_comment = models.TextField(null=True, blank=True, max_length=4096, verbose_name=_("Transfer Comment"))
    systemname = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Systemname"))
    positions_nr = models.IntegerField(null=True, blank=True, verbose_name=_("Positions-Nr."))
    referenznummer_leiferant = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Referenz-Nr. Lieferant"))
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
    bruttogewicht = models.FloatField(null=True, blank=True, verbose_name=_("Bruttogewicht"))
    gewichtseinheit = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Gewichtseinheit"))
    nettogewicht = models.FloatField(null=True, blank=True, verbose_name=_("Nettogewicht"))
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
    bestellmengeneinheit = models.ForeignKey(Bestellmengeneinheit, to_field='idx', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_("Bestellmengeneinheit"))
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
    externe_warengruppe = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Externe Warengruppe"))
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
    preisermittlung = models.IntegerField(null=True, blank=True, verbose_name=_("Preisermittlung"))
    repararaturlokation = models.CharField(null=True, blank=True, max_length=40, verbose_name=_("Repararaturlokation"))

    def get_localized_kurztext(self):
        """Returns the kurztext in the current language, falling back to German if not available"""
        from django.utils.translation import get_language
        
        current_language = get_language()
        if current_language == 'fr' and self.kurztext_fr:
            return self.kurztext_fr
        elif current_language == 'en' and self.kurztext_en:
            return self.kurztext_en
        
        # Default to German
        return self.kurztext_de

    def delete(self, *args, **kwargs):
        # First, delete all attachment files from storage
        for attachment in self.attachments.all():
            attachment.delete()  # This will call MaterialAttachment's delete() method

        # Then delete the Material record (which will cascade delete attachments)
        super().delete(*args, **kwargs)

    def __str__(self):
        if self.positions_nr is not None:
            return str(self.positions_nr) + " - " + self.kurztext_de + " (" + self.hersteller + ")"
        else:
            return "<None> - " + self.kurztext_de + " (" + self.hersteller + ")"

    class Meta:
        ordering = ["positions_nr"]
        app_label = 'b11_1'

def material_attachment_path(instance, filename):
    """
    Files will be uploaded to S3/MinIO in material_attachments/material_id/filename
    """
    return f'{instance.material.id}/{filename}'

class MaterialAttachment(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(
        upload_to=material_attachment_path,
        storage=MaterialAttachmentStorage()
    )
    comment = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_file_url(self):
        """Generate a pre-signed URL for the file that expires in 1 hour"""
        if not settings.DIVIO_HOSTING:
            # MinIO configuration
            s3_client = boto3.client('s3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4'),
                verify=False
            )
        else:
            # Production S3 configuration
            s3_client = boto3.client('s3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

        try:
            # Construct the full key including the material_attachments prefix
            key = f"material_attachments/{self.file.name}"
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': key
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return url
        except Exception as e:
            print(f"Error generating pre-signed URL: {e}")
            return None

    def delete(self, *args, **kwargs):
        try:
            # Try to delete the file from S3
            if self.file:
                self.file.delete(save=False)
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to delete file {self.file.name} from storage: {str(e)}")
            # You might want to raise the error here depending on your requirements
            # For now, we'll continue with the database deletion even if S3 deletion fails

        # Delete the database record
        super().delete(*args, **kwargs)

    class Meta:
        app_label = 'b11_1'
        ordering = ['-uploaded_at']
