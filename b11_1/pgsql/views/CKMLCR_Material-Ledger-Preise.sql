-- Create a view named 'unpivoted_werks_view' that unpivots werk columns into rows
DROP VIEW IF EXISTS CKMLCR_Material_Ledger_Preise;
CREATE VIEW CKMLCR_Material_Ledger_Preise
 AS
 SELECT a.positions_nr AS source_id,
    b.text AS bwkey,
    a.preis AS pvprs,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    '10'::text AS curtp,
    'CHF'::text AS waers,
    f.text AS vprsv
   FROM b11_1_material a
     LEFT JOIN b11_1_werk b ON a.werk_id = b.id
     LEFT JOIN b11_1_preissteuerung f ON a.preissteuerung_id = f.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
