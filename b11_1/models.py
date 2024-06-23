from django.db import models


class BEGRU(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Basismengeneinheit(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Materialart(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Sparte(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Materialzustandsverwaltung(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Rueckfuehrungscode(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Serialnummerprofil(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class SparePartClassCode(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Uebersetzungsstatus(models.Model):
    text = models.CharField(null=True, blank=True, max_length=40)

    def __str__(self):
        return self.text


class Material(models.Model):
    positions_nr = models.CharField(null=True, blank=True, max_length=40)
    kurztext_de = models.CharField(null=True, blank=True, max_length=40)
    kurztext_fr = models.CharField(null=True, blank=True, max_length=40)
    kurztext_en = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_de_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_de_2_zeile = models.CharField(null=True, blank=True)
    grunddatentext_fr_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_fr_2_zeile = models.CharField(null=True, blank=True)
    grunddatentext_en_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_en_2_zeile = models.CharField(null=True, blank=True)
    basismengeneinheit = models.ForeignKey(Basismengeneinheit, null=True, on_delete=models.DO_NOTHING, verbose_name="Basismengeneinheit ")
    bruttogewicht = models.CharField(null=True, blank=True)
    gewichtseinheit = models.CharField(null=True, blank=True)
    nettogewicht = models.CharField(null=True, blank=True)
    groesse_abmessung = models.CharField(null=True, blank=True)
    ean_upc_code = models.CharField(null=True, blank=True)
    nato_stock_number = models.CharField(null=True, blank=True)
    nsn_gruppe_klasse = models.CharField(null=True, blank=True)
    nato_versorgungs_nr = models.CharField(null=True, blank=True)
    herstellerteilenummer = models.CharField(null=True, blank=True, max_length=40)
    normbezeichnung = models.CharField(null=True, blank=True, max_length=18)
    gefahrgutkennzeichen = models.CharField(null=True, blank=True)
    instandsetzbar = models.BooleanField(null=True, blank=True)
    chargenpflicht = models.BooleanField(null=True, blank=True)
    bestellmengeneinheit = models.CharField(null=True, blank=True)
    mindestbestellmenge = models.CharField(null=True, blank=True)
    lieferzeit = models.CharField(null=True, blank=True)
    einheit_l_b_h = models.CharField(null=True, blank=True)
    laenge = models.CharField(null=True, blank=True)
    breite = models.CharField(null=True, blank=True)
    hoehe = models.CharField(null=True, blank=True)
    preis = models.CharField(null=True, blank=True)
    waehrung = models.CharField(null=True, blank=True)
    preiseinheit = models.CharField(null=True, blank=True)
    lagerfaehigkeit = models.CharField(null=True, blank=True)
    exportkontrollauflage = models.BooleanField(null=True, blank=True)
    cage_code = models.CharField(null=True, blank=True)
    hersteller_name = models.CharField(null=True, blank=True)
    hersteller_adresse = models.CharField(null=True, blank=True)
    hersteller_plz = models.CharField(null=True, blank=True)
    hersteller_ort = models.CharField(null=True, blank=True)
    revision = models.CharField(null=True, blank=True, max_length=30)
    bemerkung = models.CharField(null=True, blank=True)
    begru = models.ForeignKey(BEGRU, null=True, on_delete=models.DO_NOTHING, verbose_name="BEGRU ")
    materialart_grunddaten = models.ForeignKey(Materialart, null=True, on_delete=models.DO_NOTHING, verbose_name="Materialart ")
    sparte = models.ForeignKey(Sparte, null=True, on_delete=models.DO_NOTHING, verbose_name="Sparte ")
    produkthierarchie = models.CharField(null=True, blank=True)
    materialzustandsverwaltung = models.ForeignKey(Materialzustandsverwaltung, null=True, on_delete=models.DO_NOTHING, verbose_name="Materialzustandsverwaltung ")
    rueckfuehrungscode = models.ForeignKey(Rueckfuehrungscode, null=True, on_delete=models.DO_NOTHING, verbose_name="Rückführungscode ")
    serialnummerprofil = models.ForeignKey(Serialnummerprofil, null=True, on_delete=models.DO_NOTHING, verbose_name="Serialnummerprofil ")
    spare_part_class_code = models.ForeignKey(SparePartClassCode, null=True, on_delete=models.DO_NOTHING, verbose_name="Spare Part Class Code ")
    hersteller_nr_gp = models.CharField(null=True, blank=True)
    warengruppe = models.CharField(null=True, blank=True)
    uebersetzungsstatus = models.ForeignKey(Uebersetzungsstatus, null=True, on_delete=models.DO_NOTHING, verbose_name="Übersetzungsstatus ")
    endbevorratet = models.CharField(null=True, blank=True)
    revision_fremd = models.CharField(null=True, blank=True)
    revision_eigen = models.CharField(null=True, blank=True)
    zertifiziert_fuer_flug = models.BooleanField(null=True, blank=True)
    a_nummer = models.CharField(null=True, blank=True)
    verteilung_an_psd = models.BooleanField(null=True, blank=True)
    verteilung_an_ruag = models.BooleanField(null=True, blank=True)
    werk_1 = models.CharField(null=True, blank=True)
    werk_2 = models.CharField(null=True, blank=True)
    werk_3 = models.CharField(null=True, blank=True)
    werk_4 = models.CharField(null=True, blank=True)
    allgemeine_positionstypengruppe = models.CharField(null=True, blank=True)
    verkaufsorg = models.CharField(null=True, blank=True)
    vertriebsweg = models.CharField(null=True, blank=True)
    fuehrendes_material = models.CharField(null=True, blank=True)
    auszeichnungsfeld = models.CharField(null=True, blank=True)
    cpv_code = models.CharField(null=True, blank=True)
    fertigungssteuerer = models.CharField(null=True, blank=True)
    kennzeichen_komplexes_system = models.CharField(null=True, blank=True)
    sonderablauf = models.CharField(null=True, blank=True)
    temperaturbedingung = models.CharField(null=True, blank=True)
    bewertungsklasse = models.CharField(null=True, blank=True)
    systemmanager = models.CharField(null=True, blank=True, max_length=30)
    kennziffer_bamf = models.CharField(null=True, blank=True, max_length=30)
    mietrelevanz = models.CharField(null=True, blank=True)
    next_higher_assembly = models.CharField(null=True, blank=True, max_length=30)
    nachschubklasse = models.CharField(null=True, blank=True, max_length=30)
    verteilung_apm_kerda = models.BooleanField(null=True, blank=True)
    verteilung_svsaa = models.BooleanField(null=True, blank=True)
    verteilung_cheops = models.BooleanField(null=True, blank=True)
    zuteilung = models.CharField(null=True, blank=True)
    auspraegung = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.positions_nr + " - " + self.kurztext_de


class View_IL(models.Model):
    positions_nr = models.CharField(null=True, blank=True, max_length=40)
    kurztext_de = models.CharField(null=True, blank=True, max_length=40)
    kurztext_fr = models.CharField(null=True, blank=True, max_length=40)
    kurztext_en = models.CharField(null=True, blank=True, max_length=40)
    grunddatentext_de_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_de_2_zeile = models.CharField(null=True, blank=True)
    grunddatentext_fr_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_fr_2_zeile = models.CharField(null=True, blank=True)
    grunddatentext_en_1_zeile = models.CharField(null=True, blank=True)
    grunddatentext_en_2_zeile = models.CharField(null=True, blank=True)
    basismengeneinheit = models.CharField(null=True, blank=True)
    bruttogewicht = models.CharField(null=True, blank=True)
    gewichtseinheit = models.CharField(null=True, blank=True)
    nettogewicht = models.CharField(null=True, blank=True)
    groesse_abmessung = models.CharField(null=True, blank=True)
    ean_upc_code = models.CharField(null=True, blank=True)
    nato_stock_number = models.CharField(null=True, blank=True)
    nsn_gruppe_klasse = models.CharField(null=True, blank=True)
    nato_versorgungs_nr = models.CharField(null=True, blank=True)
    herstellerteilenummer = models.CharField(null=True, blank=True, max_length=40)
    normbezeichnung = models.CharField(null=True, blank=True, max_length=18)
    gefahrgutkennzeichen = models.CharField(null=True, blank=True)
    instandsetzbar = models.BooleanField(null=True, blank=True)
    chargenpflicht = models.BooleanField(null=True, blank=True)
    bestellmengeneinheit = models.CharField(null=True, blank=True)
    mindestbestellmenge = models.CharField(null=True, blank=True)
    lieferzeit = models.CharField(null=True, blank=True)
    einheit_l_b_h = models.CharField(null=True, blank=True)
    laenge = models.CharField(null=True, blank=True)
    breite = models.CharField(null=True, blank=True)
    hoehe = models.CharField(null=True, blank=True)
    preis = models.CharField(null=True, blank=True)
    waehrung = models.CharField(null=True, blank=True)
    preiseinheit = models.CharField(null=True, blank=True)
    lagerfaehigkeit = models.CharField(null=True, blank=True)
    exportkontrollauflage = models.BooleanField(null=True, blank=True)
    cage_code = models.CharField(null=True, blank=True)
    hersteller_name = models.CharField(null=True, blank=True)
    hersteller_adresse = models.CharField(null=True, blank=True)
    hersteller_plz = models.CharField(null=True, blank=True)
    hersteller_ort = models.CharField(null=True, blank=True)
    revision = models.CharField(null=True, blank=True, max_length=30)
    bemerkung = models.CharField(null=True, blank=True)


class View_GD(models.Model):
    begru = models.CharField(null=True, blank=True)
    materialart_grunddaten = models.CharField(null=True, blank=True)
    sparte = models.CharField(null=True, blank=True)
    produkthierarchie = models.CharField(null=True, blank=True)
    materialzustandsverwaltung = models.CharField(null=True, blank=True)
    rueckfuehrungscode = models.CharField(null=True, blank=True)
    serialnummerprofil = models.CharField(null=True, blank=True)
    spare_part_class_code = models.CharField(null=True, blank=True)
    hersteller_nr_gp = models.CharField(null=True, blank=True)
    warengruppe = models.CharField(null=True, blank=True)
    uebersetzungsstatus = models.CharField(null=True, blank=True)
    endbevorratet = models.CharField(null=True, blank=True)
    revision_fremd = models.CharField(null=True, blank=True)
    revision_eigen = models.CharField(null=True, blank=True)
    zertifiziert_fuer_flug = models.BooleanField(null=True, blank=True)
    a_nummer = models.CharField(null=True, blank=True)
    verteilung_an_psd = models.BooleanField(null=True, blank=True)
    verteilung_an_ruag = models.BooleanField(null=True, blank=True)


class View_SM_DA(models.Model):
    werk_1 = models.CharField(null=True, blank=True)
    werk_2 = models.CharField(null=True, blank=True)
    werk_3 = models.CharField(null=True, blank=True)
    werk_4 = models.CharField(null=True, blank=True)
    allgemeine_positionstypengruppe = models.CharField(null=True, blank=True)
    verkaufsorg = models.CharField(null=True, blank=True)
    vertriebsweg = models.CharField(null=True, blank=True)
    fuehrendes_material = models.CharField(null=True, blank=True)
    auszeichnungsfeld = models.CharField(null=True, blank=True)
    cpv_code = models.CharField(null=True, blank=True)
    fertigungssteuerer = models.CharField(null=True, blank=True)
    kennzeichen_komplexes_system = models.CharField(null=True, blank=True)
    sonderablauf = models.CharField(null=True, blank=True)
    temperaturbedingung = models.CharField(null=True, blank=True)
    bewertungsklasse = models.CharField(null=True, blank=True)
    systemmanager = models.CharField(null=True, blank=True, max_length=30)
    kennziffer_bamf = models.CharField(null=True, blank=True, max_length=30)
    mietrelevanz = models.CharField(null=True, blank=True)
    next_higher_assembly = models.CharField(null=True, blank=True, max_length=30)
    nachschubklasse = models.CharField(null=True, blank=True, max_length=30)
    verteilung_apm_kerda = models.BooleanField(null=True, blank=True)
    verteilung_svsaa = models.BooleanField(null=True, blank=True)
    verteilung_cheops = models.BooleanField(null=True, blank=True)
    zuteilung = models.CharField(null=True, blank=True)
    auspraegung = models.CharField(null=True, blank=True)

