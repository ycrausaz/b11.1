-- Create a view named 'unpivoted_werks_view' that unpivots werk columns into rows
DROP VIEW IF EXISTS CKMLCR_Material_Ledger_Preise;
CREATE VIEW CKMLCR_Material_Ledger_Preise
 AS
 SELECT a.positions_nr AS source_id,
    b.text AS bwkey,
    '10'::text AS curtp,
    a.preiseinheit AS peinh,
    f.text AS vprsv,
    a.preis AS stprs,
    a.preis AS pvprs,
    'CHF'::text AS waers
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN b11_1_preissteuerung f ON a.preissteuerung_id = f.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
