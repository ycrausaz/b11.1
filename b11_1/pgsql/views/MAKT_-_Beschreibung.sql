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
  WHERE b11_1_material.is_transferred = true
  ORDER BY 1;
