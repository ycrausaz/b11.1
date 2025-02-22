CREATE OR REPLACE VIEW mlan_steuer
 AS
 SELECT symm_material.id AS tmp_id,
    symm_material.positions_nr AS source_id,
    'CH'::text AS aland
   FROM symm_material
  WHERE symm_material.is_transferred = true
  ORDER BY symm_material.positions_nr;
