CREATE OR REPLACE VIEW mara_kssk_klassenzuordnung
 AS
 WITH source_data AS (
         SELECT a.id AS tmp_id,
            a.positions_nr AS source_id,
            '001'::text AS klart,
                CASE
                    WHEN a.verteilung_an_psd = true THEN 'X'::text
                    ELSE ''::text
                END AS verteilung_an_psd,
                CASE
                    WHEN a.verteilung_an_ruag = true THEN 'X'::text
                    ELSE ''::text
                END AS verteilung_an_ruag
           FROM b11_1_material a
          WHERE a.is_transferred = true
        )
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    ''::text AS tmp_x,
    'V_VERTEILUNG'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    ''::text AS tmp_x,
    'V_ZUSATZDATEN'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    ''::text AS tmp_x,
    'V_AR_NUMMER'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    source_data.verteilung_an_psd AS tmp_x,
    'V_VERTEILUNG_PSD'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    source_data.verteilung_an_ruag AS tmp_x,
    'V_VERTEILUNG_RUAG'::text AS class
   FROM source_data
UNION ALL
 SELECT source_data.tmp_id,
    source_data.source_id,
    source_data.klart,
    ''::text AS tmp_x,
    'V_BM_SBM'::text AS class
   FROM source_data
  ORDER BY 1;
