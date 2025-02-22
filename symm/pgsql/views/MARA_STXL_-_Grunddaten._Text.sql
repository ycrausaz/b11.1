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
