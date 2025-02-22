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
