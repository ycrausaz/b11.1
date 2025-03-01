CREATE OR REPLACE VIEW ckmlcr_material_ledger_preise
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS bwkey,
    '10'::text AS curtp,
    a.preiseinheit AS peinh,
    a.preissteuerung AS vprsv,
    a.preis AS stprs,
    a.preis AS pvprs,
    'CHF'::text AS waers
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
