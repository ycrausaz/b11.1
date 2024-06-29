from django.db import migrations, models
from django.db import connection

def create_views_MARA_Grunddaten(apps, schema_editor):
    view_sql = '''
DROP VIEW IF EXISTS MARA_Grunddaten;
CREATE VIEW MARA_Grunddaten AS 
SELECT
    a.positions_nr AS SOURCE_ID,
    b.text AS MTART,
    c.text AS MEINS,
    a.herstellerteilenummer AS MFRPN,
    a.hersteller_nr_gp AS MFRNR,
    a.groesse_abmessung AS GROES, 
    a.nettogewicht AS NTGEW,
    a.laenge AS LAENG,
    a.breite AS BREIT,
    a.hoehe AS HOEHE,
    a.einheit_l_b_h AS MEABM,
    a.gewichtseinheit AS GEWEI,
    d.text AS PROFL,
    a.nato_versorgungs_nr AS NSNID,
    a.ean_upc_code AS EAN11,
    CASE WHEN a.ean_upc_code IS NOT NULL THEN 'HE' ELSE NULL END AS NUMTP,
    e.text AS BEGRU,
    a.normbezeichnung AS NORMT,
    'M' AS MBRSH,
    a.warengruppe as MATKL,
    '' as BISMT,
    a.bruttogewicht AS BRGEW,
    a.bestellmengeneinheit AS BSTME,
    f.text AS SPART,
    a.chargenpflicht AS XCHPF,
    'V1' AS MSTAE,
    '' AS MTPOS_MARA,
    CASE WHEN a.chargenpflicht = 'f' THEN '1' ELSE '2' END AS MCOND,
    a.fuehrendes_material AS ZZFUEHR_MAT,
    g.text AS ZZLABEL,
    h.text AS RETDELC,
    i.text AS ADSPC_SPC,
    a.produkthierarchie AS PRDHA,
    'UAM' AS HNDLCODE,
    j.text as TEMPB,
    a.cpv_code AS ZZCPVCODE,
    k.text as ZZSONDERABLAUF,
    a.lagerfaehigkeit as "MARA-MHDHB"
FROM b11_1_material a
join b11_1_materialart b on b.id = a.materialart_grunddaten_id
join b11_1_basismengeneinheit c on c.id = a.basismengeneinheit_id
join b11_1_gefahrgutkennzeichen d on d.id = a.gefahrgutkennzeichen_id
join b11_1_begru e on e.id = a.begru_id
join b11_1_sparte f on f.id = a.sparte_id
join b11_1_auszeichnungsfeld g on g.id = a.auszeichnungsfeld_id
join b11_1_rueckfuehrungscode h on h.id = a.rueckfuehrungscode_id
join b11_1_sparepartclasscode i on i.id = a.spare_part_class_code_id
join b11_1_temperaturbedingung j on j.id = a.temperaturbedingung_id
join b11_1_sonderablauf k on k.id = a.sonderablauf_id;
        '''
    schema_editor.execute(view_sql)

def drop_views_MARA_Grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS MARA_Grunddaten;')

def create_views_MVKE_Verkaufsdaten(apps, schema_editor):
    view_sql = '''
DROP VIEW IF EXISTS MVKE_Verkaufsdaten;
CREATE VIEW MVKE_Verkaufsdaten AS
SELECT
    a.positions_nr AS SOURCE_ID,
    'M100' AS VKORG,
    b.text AS VTWEG,
    c.text AS MTPOS
FROM b11_1_material a
join b11_1_vertriebsweg b on b.id = a.vertriebsweg_id
join b11_1_allgemeinepositionstypengruppe c on c.id = a.allgemeine_positionstypengruppe_id;
        '''
    schema_editor.execute(view_sql)

def drop_views_MVKE_Verkaufsdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS MVKE_Verkaufsdaten;')

class Migration(migrations.Migration):

    dependencies = [
        ('b11_1', '0001_initial'),
    ]

    operations = [
#        migrations.RunSQL(
#            sql=create_views_MARA_Grunddaten,
#            reverse_sql=drop_views_MARA_Grunddaten,
#        ),
        migrations.RunPython(create_views_MVKE_Verkaufsdaten, reverse_code=drop_views_MVKE_Verkaufsdaten),
    ]

