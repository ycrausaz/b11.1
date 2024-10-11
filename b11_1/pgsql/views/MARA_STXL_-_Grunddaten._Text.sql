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
