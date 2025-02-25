from django.db import migrations, models
from django.db import connection

# 1
def create_views_makt_beschreibung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW makt_beschreibung
 AS
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'D'::text AS spras,
    symm_material.kurztext_de AS maktx
   FROM symm_material
  WHERE symm_material.is_transferred = true
UNION ALL
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'F'::text AS spras,
    symm_material.kurztext_fr AS maktx
   FROM symm_material
  WHERE symm_material.is_transferred = true
UNION ALL
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'E'::text AS spras,
    symm_material.kurztext_en AS maktx
   FROM symm_material
  WHERE symm_material.is_transferred = true
  ORDER BY 1;
        '''
    schema_editor.execute(view_sql)

def drop_views_makt_beschreibung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS makt_beschreibung;')

# 2
def create_views_mara_ausp_merkmale(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mara_ausp_merkmale
 AS
 WITH original_query AS (
         SELECT a.id AS tmp_id,
            a.positions_nr AS source_id,
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
                END AS v_svsaa,
                CASE
                    WHEN a.mietrelevanz = true THEN 'X'::text
                    ELSE ''::text
                END AS v_miet_relevanz,
            a.nachschubklasse AS v_nachschubklasse,
            a.preis AS v_bewertungspreis,
            a.waehrung AS v_waehrung,
            a.preiseinheit AS v_preiseinheit,
            to_char(CURRENT_DATE::timestamp with time zone, 'DD.MM.YYYY'::text) AS v_gueltigab,
            a.lagerfaehigkeit AS v_lagerfaehigkeit,
            c.text AS zuteilung,
            d.text AS auspraegung
           FROM symm_material a
             LEFT JOIN symm_uebersetzungsstatus b ON b.idx = a.uebersetzungsstatus_id
             LEFT JOIN symm_zuteilung c ON c.idx = a.zuteilung_id
             LEFT JOIN symm_auspraegung d ON d.idx = a.auspraegung_id
          WHERE a.is_transferred = true
        )
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_a_nummer AS atwrt,
    'V_A_NUMMER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_revfremd AS atwrt,
    'V_REVFREMD'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_reveigen AS atwrt,
    'V_REVEIGEN'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_systemmanager AS atwrt,
    'V_SYSTEMMANAGER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_uebersetzung AS atwrt,
    'V_UEBERSETZUNG'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_kennziffer AS atwrt,
    'V_KENNZIFFER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_next_higher AS atwrt,
    'V_NEXT_HIGHER'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_zertflug AS atwrt,
    'V_ZERTFLUG'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_apm AS atwrt,
    'V_APM'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_svsaa AS atwrt,
    'V_SVSAA'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_bewertungspreis::character varying AS atwrt,
    'V_BEWERTUNGSPREIS'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_waehrung AS atwrt,
    'V_WAEHRUNG'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_preiseinheit::character varying AS atwrt,
    'V_PREISEINHEIT'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_gueltigab::character varying AS atwrt,
    'V_GUELTIGAB'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_lagerfaehigkeit::character varying AS atwrt,
    'V_LAGERFAEHIGKEIT'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung::text = 'BM'::text THEN original_query.auspraegung::text
            ELSE ''::text
        END AS atwrt,
    'V_BETRIEBSMITTEL'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung::text = 'TRP'::text THEN original_query.auspraegung::text
            ELSE ''::text
        END AS atwrt,
    'V_SONDERBETRIEBSMITTEL_TRP'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung::text = 'MKZ'::text THEN original_query.auspraegung::text
            ELSE ''::text
        END AS atwrt,
    'V_SONDERBETRIEBSMITTEL_MKZ'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung::text = 'PRD'::text THEN original_query.auspraegung::text
            ELSE ''::text
        END AS atwrt,
    'V_SONDERBETRIEBSMITTEL_PRD'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_miet_relevanz AS atwrt,
    'V_MIET_RELEVANZ'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
    original_query.v_nachschubklasse AS atwrt,
    'V_NACHSCHUBKLASSE'::text AS atnam
   FROM original_query
  ORDER BY 1, 4;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_ausp_merkmale(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_ausp_merkmale;')

# 3
def create_views_mara_mara(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mara_mara
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS mtart,
    c.text AS meins,
    a.herstellerteilenummer AS mfrpn,
    a.geschaeftspartner AS mfrnr,
    a.groesse_abmessung AS groes,
    a.nettogewicht AS ntgew,
    a.laenge AS laeng,
    a.breite AS breit,
    a.hoehe,
    'MM'::text AS meabm,
    'KG'::text AS gewei,
    d.text AS profl,
    a.nato_versorgungs_nr AS nsnid,
    a.ean_upc_code AS ean11,
        CASE
            WHEN a.ean_upc_code IS NULL THEN ''::text
            ELSE 'HE'::text
        END AS numtp,
    e.text AS begru,
    a.normbezeichnung AS normt,
    'M'::text AS mbrsh,
    a.warengruppe AS matkl,
    ''::text AS bismt,
    a.bruttogewicht AS brgew,
    a.bestellmengeneinheit AS bstme,
    f.text AS spart,
        CASE
            WHEN a.chargenpflicht = false THEN 'N'::text
            ELSE 'X'::text
        END AS xchpf,
    'V1'::text AS mstae,
    ''::text AS mtpos_mara,
        CASE
            WHEN a.chargenpflicht = false THEN '1'::text
            ELSE '2'::text
        END AS mcond,
    a.fuehrendes_material AS zzfuehr_mat,
    a.auszeichnungsfeld AS zzlabel,
    h.text AS retdelc,
    i.text AS adspc_spc,
    a.produkthierarchie AS prdha,
    'UAM'::text AS hndlcode,
    j.text AS tempb,
    k.text AS zzsonderablauf,
    '2'::text AS "IPRKZ",
    a.externe_warengruppe AS extwg,
        CASE
            WHEN a.kennzeichen_komplexes_system = true THEN 'X'::text
            ELSE ''::text
        END AS zzkomsys
   FROM symm_material a
     LEFT JOIN symm_materialart b ON b.idx = a.materialart_grunddaten_id
     LEFT JOIN symm_basismengeneinheit c ON c.idx = a.basismengeneinheit_id
     LEFT JOIN symm_gefahrgutkennzeichen d ON d.idx = a.gefahrgutkennzeichen_id
     LEFT JOIN symm_begru e ON e.idx = a.begru_id
     LEFT JOIN symm_sparte f ON f.idx = a.sparte_id
     LEFT JOIN symm_rueckfuehrungscode h ON h.idx = a.rueckfuehrungscode_id
     LEFT JOIN symm_sparepartclasscode i ON i.idx = a.spare_part_class_code_id
     LEFT JOIN symm_temperaturbedingung j ON j.idx = a.temperaturbedingung_id
     LEFT JOIN symm_sonderablauf k ON k.idx = a.sonderablauf_id
  WHERE a.is_transferred = true;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_mara;')

# 4
def create_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mara_kssk_klassenzuordnung
 AS
 WITH source_data AS (
         SELECT a.id AS tmp_id,
            a.positions_nr AS source_id,
            '001'::text AS klart
           FROM symm_material a
          WHERE a.is_transferred = true
        )
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    'V_VERTEILUNG_PSD'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    'V_ZUSATZDATEN'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    'V_AR_NUMMER'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    'V_VERTEILUNG'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    'V_BM_SBM'::text AS class
   FROM source_data
  ORDER BY 1;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_kssk_klassenzuordnung;')

# 5
def create_views_mara_stxh_grunddaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mara_stxh_grunddaten
 AS
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    symm_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'D'::text AS tdspras
   FROM symm_material
  WHERE symm_material.is_transferred = true
UNION ALL
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    symm_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'F'::text AS tdspras
   FROM symm_material
  WHERE symm_material.is_transferred = true
UNION ALL
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    symm_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'E'::text AS tdspras
   FROM symm_material
  WHERE symm_material.is_transferred = true
  ORDER BY 1;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxh_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxh_grunddaten;')

# 6
def create_views_mara_stxl_grunddaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mara_stxl_grunddaten
 AS
 SELECT mara_stxl_grunddaten.tmp_id,
    mara_stxl_grunddaten.source_id,
    'MATERIAL'::text AS tdobject,
    mara_stxl_grunddaten.source_id AS tdname,
    'GRUN'::text AS tdid,
    mara_stxl_grunddaten.tdspras,
    mara_stxl_grunddaten.line_counter,
    mara_stxl_grunddaten.tdformat,
    mara_stxl_grunddaten.text AS tdline
   FROM ( SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr AS source_id,
            'D'::text AS tdspras,
            1 AS line_counter,
            ''::text AS tdformat,
            symm_material.grunddatentext_de_1_zeile AS text
           FROM symm_material
          WHERE symm_material.is_transferred = true
        UNION ALL
         SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr,
            'D'::text AS text,
            2,
            '/'::text AS tdformat,
            symm_material.grunddatentext_de_2_zeile
           FROM symm_material
          WHERE symm_material.is_transferred = true
        UNION ALL
         SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr,
            'F'::text AS text,
            1,
            ''::text AS tdformat,
            symm_material.grunddatentext_fr_1_zeile
           FROM symm_material
          WHERE symm_material.is_transferred = true
        UNION ALL
         SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr,
            'F'::text AS text,
            2,
            '/'::text AS tdformat,
            symm_material.grunddatentext_fr_2_zeile
           FROM symm_material
          WHERE symm_material.is_transferred = true
        UNION ALL
         SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr,
            'E'::text AS text,
            1,
            ''::text AS tdformat,
            symm_material.grunddatentext_en_1_zeile
           FROM symm_material
          WHERE symm_material.is_transferred = true
        UNION ALL
         SELECT symm_material.id AS tmp_id,
            symm_material.positions_nr,
            'E'::text AS text,
            2,
            '/'::text AS tdformat,
            symm_material.grunddatentext_en_2_zeile
           FROM symm_material
          WHERE symm_material.is_transferred = true) mara_stxl_grunddaten
  ORDER BY mara_stxl_grunddaten.source_id, mara_stxl_grunddaten.tdspras, mara_stxl_grunddaten.line_counter;
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxl_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxl_grunddaten;')

# 7
def create_views_marc_werksdaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW marc_werksdaten
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    a.lieferzeit AS plifz,
    b.text AS werks,
    'ND'::text AS dismm,
    c.text AS fevor,
        CASE
            WHEN a.orderbuchpflicht = true THEN 'X'::text
            ELSE NULL::text
        END AS kordb
   FROM symm_material a
     LEFT JOIN symm_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
     LEFT JOIN symm_fertigungssteuerer c ON a.fertigungssteuerer_id = c.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
        '''
    schema_editor.execute(view_sql)

def drop_views_marc_werksdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS marc_werksdaten;')

# 8
def create_views_mbew_buchhaltung(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mbew_buchhaltung
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS bwkey,
    a.preissteuerung AS vprsv,
    a.preis AS verpr,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    f.text AS bklas,
    a.preisermittlung AS mlast
   FROM symm_material a
     LEFT JOIN symm_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
     LEFT JOIN symm_bewertungsklasse f ON a.bewertungsklasse_id = f.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
        '''
    schema_editor.execute(view_sql)

def drop_views_mbew_buchhaltung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mbew_buchhaltung;')

# 9
def create_views_mlan_steuer(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mlan_steuer
 AS
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'CH'::text AS aland
   FROM symm_material
  WHERE symm_material.is_transferred = true
  ORDER BY symm_material.positions_nr;
        '''
    schema_editor.execute(view_sql)

def drop_views_mlan_steuer(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mlan_steuer;')

# 10
def create_views_mvke_verkaufsdaten(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW mvke_verkaufsdaten
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    a.verkaufsorg AS vkorg,
    a.vertriebsweg AS vtweg,
    c.text AS mtpos
   FROM symm_material a
     LEFT JOIN symm_allgemeinepositionstypengruppe c ON c.idx = a.allgemeine_positionstypengruppe_id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr;
        '''
    schema_editor.execute(view_sql)

def drop_views_mvke_verkaufsdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mvke_verkaufsdaten;')

# 11
def create_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    view_sql = '''
CREATE OR REPLACE VIEW ckmlcr_material_ledger_preise
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS bwkey,
    '10'::text AS curtp,
    a.preiseinheit AS peinh,
    a.preissteuerung AS vprsv,
    a.preis AS stprs,
    a.preis AS pvprs,
    'CHF'::text AS waers
   FROM symm_material a
     LEFT JOIN symm_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
        '''
    schema_editor.execute(view_sql)

def drop_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS ckmlcr_material_ledger_preise;')


class Migration(migrations.Migration):

    dependencies = [
        ('symm', '0001_initial'),
    ]

    operations = [
# 1
        migrations.RunPython(create_views_makt_beschreibung, reverse_code=drop_views_makt_beschreibung),
# 2
        migrations.RunPython(create_views_mara_ausp_merkmale, reverse_code=drop_views_mara_ausp_merkmale),
# 3
        migrations.RunPython(create_views_mara_mara, reverse_code=drop_views_mara_grunddaten),
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

