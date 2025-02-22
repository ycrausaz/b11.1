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
