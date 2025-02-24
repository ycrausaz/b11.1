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
