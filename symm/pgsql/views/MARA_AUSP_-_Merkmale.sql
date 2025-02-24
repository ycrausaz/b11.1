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
                END as v_miet_relevanz,
            a.nachschubklasse as v_nachschubklasse,
            a.preis AS v_bewertungspreis,
            a.waehrung AS v_waehrung,
            a.preiseinheit AS v_preiseinheit,
            to_char(CURRENT_DATE::timestamp with time zone, 'DD.MM.YYYY'::text) AS v_gueltigab,
            a.lagerfaehigkeit AS v_lagerfaehigkeit,
            c.text as zuteilung,
            d.text as auspraegung
           FROM symm_material a
             LEFT JOIN symm_uebersetzungsstatus b ON b.idx = a.uebersetzungsstatus_id
             LEFT JOIN symm_zuteilung c on c.idx = a.zuteilung_id
             LEFT JOIN symm_auspraegung d on d.idx = a.auspraegung_id
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
--UNION ALL
-- SELECT original_query.tmp_id,
--    original_query.source_id,
--    original_query.klart,
--    original_query.v_cheops AS atwrt,
--    'V_CHEOPS'::text AS atnam
--   FROM original_query
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
            WHEN original_query.zuteilung = 'BM' THEN original_query.auspraegung
            ELSE ''::text
        END AS atwart,
    'V_BETRIEBSMITTEL'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung = 'TRP' THEN original_query.auspraegung
            ELSE ''::text
        END AS atwart,
    'V_SONDERBETRIEBSMITTEL_TRP'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung = 'MKZ' THEN original_query.auspraegung
            ELSE ''::text
        END AS atwart,
    'V_SONDERBETRIEBSMITTEL_MKZ'::text AS atnam
   FROM original_query
UNION ALL
 SELECT original_query.tmp_id,
    original_query.source_id,
    original_query.klart,
        CASE
            WHEN original_query.zuteilung = 'PRD' THEN original_query.auspraegung
            ELSE ''::text
        END AS atwart,
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
