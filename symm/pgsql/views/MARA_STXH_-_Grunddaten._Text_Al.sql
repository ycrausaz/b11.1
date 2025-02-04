CREATE OR REPLACE VIEW mara_stxh_grunddaten
 AS
 SELECT b11_1_material.id AS tmp_id,
    b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'D'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.id AS tmp_id,
    b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'F'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
UNION ALL
 SELECT b11_1_material.id AS tmp_id,
    b11_1_material.positions_nr AS source_id,
    'MATERIAL'::text AS tdobject,
    b11_1_material.positions_nr AS tdname,
    'GRUN'::text AS tdid,
    'E'::text AS tdspras
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
  ORDER BY 1;
