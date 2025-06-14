CREATE OR REPLACE VIEW mlan_steuer
 AS
 SELECT b11_1_material.id AS tmp_id,
    b11_1_material.positions_nr AS source_id,
    'CH'::text AS aland
   FROM b11_1_material
  WHERE b11_1_material.is_transferred = true
  ORDER BY b11_1_material.positions_nr;
