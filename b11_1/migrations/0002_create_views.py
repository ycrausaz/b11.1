from django.db import migrations, models
from django.db import connection

# 1
def create_views_makt_beschreibung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.makt_beschreibung
 AS
 SELECT b11_1_material.positions_nr AS source_id,
    'D'::text AS spras,
    b11_1_material.kurztext_de AS maktx
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.positions_nr AS source_id,
    'F'::text AS spras,
    b11_1_material.kurztext_fr AS maktx
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.positions_nr AS source_id,
    'E'::text AS spras,
    b11_1_material.kurztext_en AS maktx
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true;
        '''
    schema_editor.execute(view_sql)

def drop_views_makt_beschreibung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS makt_beschreibung;')

# 2
def create_views_mara_ausp_merkmale(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mara_ausp_merkmale
 AS
 WITH original_query AS (
         SELECT a.positions_nr AS source_id,
            '001'::text AS klart,
            a.a_nummer AS v_a_nummer,
            a.revision_fremd AS v_revfremd,
            a.revision_eigen AS v_reveigen,
            a.systemmanager AS v_systemmanager,
            b.text AS v_uebersetzung,
            a.kennziffer_bamf AS v_kennziffer,
            a.next_higher_assembly AS v_next_higher,
                CASE
                    WHEN a.zertifiziert_fuer_flug = true THEN 'J'::text
                    ELSE ''::text
                END AS v_zertflug,
                CASE
                    WHEN a.verteilung_apm_kerda = true THEN 'X'::text
                    ELSE ''::text
                END AS v_apm,
                CASE
                    WHEN a.verteilung_cheops = true THEN 'X'::text
                    ELSE ''::text
                END AS v_cheops,
                CASE
                    WHEN a.verteilung_svsaa = true THEN 'X'::text
                    ELSE ''::text
                END AS v_svsaa
           FROM b11_1_material a
             LEFT JOIN b11_1_uebersetzungsstatus b ON b.id = a.uebersetzungsstatus_id
          WHERE a.is_transferred = true
        )
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_a_nummer AS atwrt,
    'V_A_NUMMER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_revfremd AS atwrt,
    'V_REVFREMD'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_reveigen AS atwrt,
    'V_REVEIGEN'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_systemmanager AS atwrt,
    'V_SYSTEMMANAGER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_uebersetzung AS atwrt,
    'V_UEBERSETZUNG'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_kennziffer AS atwrt,
    'V_KENNZIFFER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_next_higher AS atwrt,
    'V_NEXT_HIGHER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_zertflug AS atwrt,
    'V_ZERTFLUG'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_apm AS atwrt,
    'V_APM'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_cheops AS atwrt,
    'V_CHEOPS'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.source_id,
    original_query.klart,
    original_query.v_svsaa AS atwrt,
    'V_SVSAA'::text AS atnam
   FROM original_query
  ORDER BY 1, 4;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_ausp_merkmale(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_ausp_merkmale;')

# 3
def create_views_mara_grunddaten(apps, schema_editor):
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
    'MM' AS MEABM,
    'KG' AS GEWEI,
    d.text AS PROFL,
    a.nato_versorgungs_nr AS NSNID,
    a.ean_upc_code AS EAN11,
    CASE WHEN a.ean_upc_code is null THEN '' ELSE 'HE' END AS NUMTP,
    e.text AS BEGRU,
    a.normbezeichnung AS NORMT,
    'M' AS MBRSH,
    a.warengruppe AS MATKL,
    '' AS BISMT,
    a.bruttogewicht AS BRGEW,
    a.bestellmengeneinheit AS BSTME,
    f.text AS SPART,
    CASE WHEN a.chargenpflicht = 'f' then 'N' else 'X' END AS XCHPF,
    'V1' AS MSTAE,
    '' AS MTPOS_MARA,
    CASE WHEN a.chargenpflicht = 'f' THEN '1' ELSE '2' END AS MCOND,
    a.fuehrendes_material AS ZZFUEHR_MAT,
    g.text AS ZZLABEL,
    h.text AS RETDELC,
    i.text AS ADSPC_SPC,
    a.produkthierarchie AS PRDHA,
    'UAM' AS HNDLCODE,
    j.text AS TEMPB,
    a.cpv_code AS ZZCPVCODE,
    k.text AS ZZSONDERABLAUF,
    a.lagerfaehigkeit AS "MARA-MHDHB",
    '1' as "MARA-MHDRZ",
    '2' as "MARA-IPRKZ"
FROM b11_1_material a
left join b11_1_materialart b on b.id = a.materialart_grunddaten_id
left join b11_1_basismengeneinheit c on c.id = a.basismengeneinheit_id
left join b11_1_gefahrgutkennzeichen d on d.id = a.gefahrgutkennzeichen_id
left join b11_1_begru e on e.id = a.begru_id
left join b11_1_sparte f on f.id = a.sparte_id
left join b11_1_auszeichnungsfeld g on g.id = a.auszeichnungsfeld_id
left join b11_1_rueckfuehrungscode h on h.id = a.rueckfuehrungscode_id
left join b11_1_sparepartclasscode i on i.id = a.spare_part_class_code_id
left join b11_1_temperaturbedingung j on j.id = a.temperaturbedingung_id
left join b11_1_sonderablauf k on k.id = a.sonderablauf_id
where a.is_transferred='t';
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_grunddaten;')

# 4
def create_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mara_kssk_klassenzuordnung
 AS
 WITH source_data AS (
         SELECT a.positions_nr AS source_id,
            '001'::text AS klart
           FROM b11_1_material a
          WHERE a.is_transferred = true
        )
 SELECT source_data.source_id,
    source_data.klart,
    'V_VERTEILUNG_PSD'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.source_id,
    source_data.klart,
    'V_ZUSATZDATEN'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.source_id,
    source_data.klart,
    'V_AR_NUMMER'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.source_id,
    source_data.klart,
    'V_VERTEILUNG'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.source_id,
    source_data.klart,
    'V_BM_SBM'::text AS class
   FROM source_data;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_kssk_klassenzuordnung;')

# 5
def create_views_mara_stxh_grunddaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mara_stxh_grunddaten
 AS
 SELECT b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'D'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'F'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'E'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxh_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxh_grunddaten;')

# 6
def create_views_mara_stxl_grunddaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mara_stxl_grunddaten
 AS
 SELECT mara_stxl_grunddaten.source_id,
    'MATERIAL'::text AS tdobject,
    mara_stxl_grunddaten.source_id AS tdname,
    'GRUN'::text AS tdid,
    mara_stxl_grunddaten.tdspras,
    mara_stxl_grunddaten.line_counter,
    mara_stxl_grunddaten.tdformat,
    mara_stxl_grunddaten.text AS tdline
   FROM ( SELECT b11_1_material.positions_nr AS source_id,
            'D'::text AS tdspras,
            1 AS line_counter,
            ''::text AS tdformat,
            b11_1_material.grunddatentext_de_1_zeile AS text
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true
        UNION ALL
         SELECT b11_1_material.positions_nr,
            'D'::text,
            2,
            '/'::text AS tdformat,
            b11_1_material.grunddatentext_de_2_zeile
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true
        UNION ALL
         SELECT b11_1_material.positions_nr,
            'F'::text,
            1,
            ''::text AS tdformat,
            b11_1_material.grunddatentext_fr_1_zeile
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true
        UNION ALL
         SELECT b11_1_material.positions_nr,
            'F'::text,
            2,
            '/'::text AS tdformat,
            b11_1_material.grunddatentext_fr_2_zeile
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true
        UNION ALL
         SELECT b11_1_material.positions_nr,
            'E'::text,
            1,
            ''::text AS tdformat,
            b11_1_material.grunddatentext_en_1_zeile
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true
        UNION ALL
         SELECT b11_1_material.positions_nr,
            'E'::text,
            2,
            '/'::text AS tdformat,
            b11_1_material.grunddatentext_en_2_zeile
           FROM b11_1_material
          WHERE b11_1_material.is_transferred = true) mara_stxl_grunddaten
  ORDER BY mara_stxl_grunddaten.source_id, mara_stxl_grunddaten.tdspras, mara_stxl_grunddaten.line_counter;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxl_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxl_grunddaten;')

# 7
def create_views_marc_werksdaten(apps, schema_editor):
    view_sql = '''
DROP VIEW IF EXISTS MARC_Werksdaten;
CREATE VIEW MARC_Werksdaten AS
WITH material_data AS (
    SELECT 
        a.positions_nr AS source_id, 
        b.text AS werk_1, 
        c.text AS werk_2, 
        d.text AS werk_3, 
        e.text AS werk_4, 
        'ND' AS dismm, 
        a.orderbuchpflicht AS kordb
    FROM 
        b11_1_material a
    LEFT JOIN 
        b11_1_werk_1 b ON a.werk_1_id = b.id
    LEFT JOIN 
        b11_1_werk_2 c ON a.werk_2_id = c.id
    LEFT JOIN 
        b11_1_werk_3 d ON a.werk_3_id = d.id
    LEFT JOIN 
        b11_1_werk_4 e ON a.werk_4_id = e.id
    WHERE a.is_transferred = 't'
)
SELECT 
    source_id, 
    werk AS werks, 
    dismm,
    kordb
FROM (
    SELECT 
        source_id, 
        werk_1 AS werk, 
        dismm,
        kordb
    FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_2 AS werk, 
        dismm,
        kordb
    FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_3 AS werk, 
        dismm,
        kordb
    FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_4 AS werk, 
        dismm,
        kordb
    FROM 
        material_data
) AS unpivoted_data
ORDER BY 
    source_id, 
    werks;
        '''
    schema_editor.execute(view_sql)

def drop_views_marc_werksdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS marc_werksdaten;')

# 8
def create_views_mbew_buchhaltung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mbew_buchhaltung
 AS
 WITH material_data AS (
         SELECT a.positions_nr AS source_id,
            b.text AS werk_1,
            c.text AS werk_2,
            d.text AS werk_3,
            e.text AS werk_4,
            a.preis AS verpr,
            a.preis AS stprs,
            a.preiseinheit AS peinh,
            f.text AS bklas
           FROM b11_1_material a
             LEFT JOIN b11_1_werk_1 b ON a.werk_1_id = b.id
             LEFT JOIN b11_1_werk_2 c ON a.werk_2_id = c.id
             LEFT JOIN b11_1_werk_3 d ON a.werk_3_id = d.id
             LEFT JOIN b11_1_werk_4 e ON a.werk_4_id = e.id
             LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.id
          WHERE a.is_transferred = true
        )
 SELECT unpivoted_data.source_id,
    unpivoted_data.werk AS bwkey,
    unpivoted_data.verpr,
    unpivoted_data.stprs,
    unpivoted_data.peinh,
    unpivoted_data.bklas
   FROM ( SELECT material_data.source_id,
            material_data.werk_1 AS werk,
            material_data.verpr,
            material_data.stprs,
            material_data.peinh,
            material_data.bklas
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_2 AS werk,
            material_data.verpr,
            material_data.stprs,
            material_data.peinh,
            material_data.bklas
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_3 AS werk,
            material_data.verpr,
            material_data.stprs,
            material_data.peinh,
            material_data.bklas
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_4 AS werk,
            material_data.verpr,
            material_data.stprs,
            material_data.peinh,
            material_data.bklas
           FROM material_data) unpivoted_data
  ORDER BY unpivoted_data.source_id, unpivoted_data.werk;
        '''
    schema_editor.execute(view_sql)

def drop_views_mbew_buchhaltung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mbew_buchhaltung;')

# 9
def create_views_mlan_steuer(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mlan_steuer
 AS
 SELECT b11_1_material.positions_nr AS source_id,
    'CH'::text AS aland
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true;
        '''
    schema_editor.execute(view_sql)

def drop_views_mlan_steuer(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mlan_steuer;')

# 10
def create_views_mvke_verkaufsdaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.mvke_verkaufsdaten
 AS
 SELECT a.positions_nr AS source_id,
    'M100'::text AS vkorg,
    b.text AS vtweg,
    c.text AS mtpos
   FROM b11_1_material a
     LEFT JOIN b11_1_vertriebsweg b ON b.id = a.vertriebsweg_id
     LEFT JOIN b11_1_allgemeinepositionstypengruppe c ON c.id = a.allgemeine_positionstypengruppe_id
  WHERE a.is_transferred = true;
        '''
    schema_editor.execute(view_sql)

def drop_views_mvke_verkaufsdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mvke_verkaufsdaten;')

# 11
def create_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW public.ckmlcr_material_ledger_preise
 AS
 WITH material_data AS (
         SELECT a.positions_nr AS source_id,
            b.text AS werk_1,
            c.text AS werk_2,
            d.text AS werk_3,
            e.text AS werk_4,
            a.preis AS pvprs,
            a.preis AS stprs,
            a.preiseinheit AS peinh,
            '10'::text AS curtp,
            'CHF'::text AS waers,
            a.preissteuerung_id AS vprsv
           FROM b11_1_material a
             LEFT JOIN b11_1_werk_1 b ON a.werk_1_id = b.id
             LEFT JOIN b11_1_werk_2 c ON a.werk_2_id = c.id
             LEFT JOIN b11_1_werk_3 d ON a.werk_3_id = d.id
             LEFT JOIN b11_1_werk_4 e ON a.werk_4_id = e.id
             LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.id
          WHERE a.is_transferred = true
        )
 SELECT unpivoted_data.source_id,
    unpivoted_data.werk AS bwkey,
    unpivoted_data.pvprs,
    unpivoted_data.stprs,
    unpivoted_data.peinh,
    unpivoted_data.curtp,
    unpivoted_data.waers,
    unpivoted_data.vprsv
   FROM ( SELECT material_data.source_id,
            material_data.werk_1 AS werk,
            material_data.pvprs,
            material_data.stprs,
            material_data.peinh,
            material_data.curtp,
            material_data.waers,
            material_data.vprsv
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_2 AS werk,
            material_data.pvprs,
            material_data.stprs,
            material_data.peinh,
            material_data.curtp,
            material_data.waers,
            material_data.vprsv
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_3 AS werk,
            material_data.pvprs,
            material_data.stprs,
            material_data.peinh,
            material_data.curtp,
            material_data.waers,
            material_data.vprsv
           FROM material_data
        UNION ALL
         SELECT material_data.source_id,
            material_data.werk_4 AS werk,
            material_data.pvprs,
            material_data.stprs,
            material_data.peinh,
            material_data.curtp,
            material_data.waers,
            material_data.vprsv
           FROM material_data) unpivoted_data
  ORDER BY unpivoted_data.source_id, unpivoted_data.werk;

ALTER TABLE public.ckmlcr_material_ledger_preise
    OWNER TO postgres;
        '''
    schema_editor.execute(view_sql)

def drop_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS ckmlcr_material_ledger_preise;')


class Migration(migrations.Migration):

    dependencies = [
        ('b11_1', '0001_initial'),
    ]

    operations = [
# 1
        migrations.RunPython(create_views_makt_beschreibung, reverse_code=drop_views_makt_beschreibung),
# 2
        migrations.RunPython(create_views_mara_ausp_merkmale, reverse_code=drop_views_mara_ausp_merkmale),
# 3
        migrations.RunPython(create_views_mara_grunddaten, reverse_code=drop_views_mara_grunddaten),
# 4
        migrations.RunPython(create_views_mara_kssk_klassenzuordnung, reverse_code=drop_views_mara_kssk_klassenzuordnung),
# 5
        migrations.RunPython(create_views_mara_stxh_grunddaten, reverse_code=drop_views_mara_stxh_grunddaten),
# 6
        migrations.RunPython(create_views_mara_stxl_grunddaten, reverse_code=drop_views_mara_stxl_grunddaten),
# 7
        migrations.RunPython(create_views_marc_werksdaten, reverse_code=drop_views_marc_werksdaten),
# 8
        migrations.RunPython(create_views_mbew_buchhaltung, reverse_code=drop_views_mbew_buchhaltung),
# 9
        migrations.RunPython(create_views_mlan_steuer, reverse_code=drop_views_mlan_steuer),
# 10
        migrations.RunPython(create_views_mvke_verkaufsdaten, reverse_code=drop_views_mvke_verkaufsdaten),
# 11
        migrations.RunPython(create_views_ckmlcr_material_ledger_preise, reverse_code=drop_views_ckmlcr_material_ledger_preise),
    ]

